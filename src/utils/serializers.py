import peewee

from marshmallow import Schema, fields, ValidationError


class ModelSerializer:
    serializer_field = {
        'CharField': fields.Str,
        'TextField': fields.Str,
        'DateTimeField': fields.DateTime,
        'AutoField': fields.Integer,
        'ForeignKeyField': fields.Integer
    }

    _validated = False
    _writable_fields = None
    _readable_fields = None
    _errors = None

    class Meta:
        model = None
        fields = ()
        extra_kwargs = {}

    def __init__(self, instance=None, data=None, **kwargs):
        self.instance = instance
        if data:
            self.initial_data = data

        self.partial = kwargs.pop('partial', False)  # TODO: Usar, algun dia
        self._context = kwargs.pop('context', {})
        kwargs.pop('many', None)

        self.setup_fields()
        self._errors = []

    def __new__(cls, *args, **kwargs):
        # Funcion copiadita de Django. Permite serializar una lista si se pasa
        # el atributo many como verdadero
        if kwargs.pop('many', False):
            return cls.many_init(*args, **kwargs)
        instance = super().__new__(cls)
        instance._args = args
        instance._kwargs = kwargs
        return instance

    @classmethod
    def many_init(cls, *args, **kwargs):
        serializer = ListSerializer(*args, **kwargs)
        if hasattr(cls.Meta, 'model'):
            serializer.Meta.model = cls.Meta.model
        if hasattr(cls.Meta, 'fields'):
            serializer.Meta.fields = cls.Meta.fields
        if hasattr(cls.Meta, 'extra_kwargs'):
            serializer.Meta.extra_kwargs = cls.Meta.extra_kwargs
        return serializer

    def create(self, validated_data):
        return self.Meta.model.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

    def setup_fields(self):
        self._writable_fields = {}
        self._readable_fields = {}

        field_names = self.Meta.fields or []
        if field_names == '__all__':
            field_names = []
            for possible_field_name in dir(self.Meta.model):
                possible_field = getattr(self.Meta.model, possible_field_name)
                if isinstance(possible_field, peewee.Field):
                    field_names.append(possible_field_name)

            field_names = tuple(field_names)

        for field_name in field_names:
            marshmallow_type = None
            if hasattr(self.Meta, 'model'):
                field = getattr(self.Meta.model, field_name)
                field_type = type(field).__name__
                marshmallow_type = self.serializer_field[field_type]()

            if hasattr(self, field_name):
                marshmallow_type = getattr(self, field_name)

            if not marshmallow_type:
                self._errors.append(
                    '{} needs a marshmallow field configured'.format(
                        field_name
                    )
                )
                return

            extra_kwargs = self.get_extra_kwargs_of(field_name)
            if not extra_kwargs.get('read_only'):
                self._writable_fields[field_name] = marshmallow_type
            if not extra_kwargs.get('write_only'):
                self._readable_fields[field_name] = marshmallow_type

    @property
    def writable_fields(self):
        return self._writable_fields

    @property
    def readable_fields(self):
        return self._readable_fields

    def get_extra_kwargs(self):
        if hasattr(self.Meta, 'extra_kwargs'):
            return self.Meta.extra_kwargs
        return {}

    def get_extra_kwargs_of(self, field):
        extra_kwargs = self.get_extra_kwargs()
        field_kwargs = {
            'read_only': False,
            'write_only': False,
            'min_length': None,
            'max_length': None,
            'required': True
        }
        field_meta_kwargs = extra_kwargs.get(field)
        if field_meta_kwargs:
            for attr in field_meta_kwargs:
                field_kwargs[attr] = field_meta_kwargs[attr]

        return field_kwargs

    def is_valid(self, raise_exception=False):
        self._validated = True

        if not hasattr(self, '_validated_data'):
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except Exception as exc:
                self._validated_data = {}
                self._errors.append(exc)

        if self._errors and raise_exception:
            raise ValidationError(self._errors)

        return not bool(self._errors)

    def run_validation(self, data):
        data = self.to_internal_value(data)

        validated_data = None
        try:
            validated_data = self.validate(data)
        except Exception as e:
            self._errors.append(e)

        return validated_data

    def to_internal_value(self, data):
        fields = self._writable_fields

        ret = {}
        for field_name in fields:
            validate_method = getattr(self, 'validate_' + field_name, None)
            primitive_value = data.get(field_name)

            try:
                validated_value = self.validate_primitive_value(
                    field_name,
                    primitive_value
                )
                if validate_method is not None:
                    validated_value = validate_method(validated_value)
            except ValidationError as exc:
                self._errors.append(exc)
            else:
                ret[field_name] = validated_value

        if self._errors:
            raise ValidationError(self._errors)

        return ret

    def validate_primitive_value(self, field_name, value):
        extra_kwargs = self.get_extra_kwargs_of(field_name)
        required = extra_kwargs.get('required')

        if required and value is None:
            raise ValidationError('{} is required'.format(field_name))

        marshmallow_conf = self._writable_fields[field_name]
        schema = Schema.from_dict({field_name: marshmallow_conf})()
        validated_value = schema.load({field_name: value})[field_name]

        return validated_value

    def validate(self, attrs):
        return attrs

    def save(self):
        if not self._validated:
            raise ValueError('You have to call is_valid method before saving')

        if self.instance is not None:
            self.instance = self.update(self.instance, self._validated_data)
            assert self.instance is not None, (
                '`update()` did not return an object instance.'
            )
        else:
            self.instance = self.create(self._validated_data)
            assert self.instance is not None, (
                '`create()` did not return an object instance.'
            )

        return self.instance

    # def serialize_datetime(self, attr):
    #     if hasattr(conf, 'DATE_FORMAT'):
    #         serialized = attr.strftime(conf.DATE_FORMAT)
    #     else:
    #         serialized = attr.isoformat()
    #
    #     return serialized

    def to_representation(self, instance):
        ret = {}
        try:
            for field in self.readable_fields:
                attr = getattr(instance, field)
                if isinstance(attr, peewee.Model):
                    attr = attr.id
                ret[field] = attr
        except ValueError as e:
            self._errors.append(e)

        schema = Schema.from_dict(self.readable_fields)()

        return schema.dump(ret)

    @property
    def data(self):
        return self.to_representation(self.instance)

    @property
    def errors(self):
        errors = []
        for error in self._errors:
            if hasattr(error, 'messages'):
                errors += error.messages
            else:
                errors.append(error)

        return errors


class ListSerializer(ModelSerializer):
    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance, data, **kwargs)

    def to_representation(self, data):
        if not type(data).__name__ == 'ModelSelect':
            raise ValueError('You need to pass a peewee queryset as instance')

        ret = []
        for item in data:
            serialized_element = super().to_representation(item)
            ret.append(serialized_element)
        return ret
