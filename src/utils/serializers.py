import peewee

from marshmallow import Schema, fields  # ValidationError


class ModelSerializer:
    serializer_field = {
        'CharField': fields.Str,
        'TextField': fields.Str,
        'DateTimeField': fields.DateTime,
        'AutoField': fields.Integer
    }

    _validated = False
    _fields = {}
    _errors = []

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

    def get_fields(self):
        field_names = self.Meta.fields
        if field_names == '__all__':
            field_names = []
            for possible_field_name in dir(self.Meta.model):
                possible_field = getattr(self.Meta.model, possible_field_name)
                if isinstance(possible_field, peewee.Field):
                    self._fields[possible_field_name] = self.serializer_field[
                        type(possible_field).__name__
                    ]()
                    field_names.append(possible_field_name)

            field_names = tuple(field_names)
        return field_names

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
            'max_length': None
        }
        field_meta_kwargs = extra_kwargs.get(field)
        if field_meta_kwargs:
            for attr in field_meta_kwargs:
                field_kwargs[attr] = field_meta_kwargs[attr]

        return field_kwargs

    def get_validators(self):
        validators = {}
        for field in self.get_fields():
            validator_name = 'validate_{}'.format(field)
            if hasattr(self, validator_name):
                validators[field] = (getattr(self, validator_name))

        return validators

    def is_valid(self, raise_exception=False):
        self._validated = True

        if not hasattr(self, '_validated_data'):
            try:
                self.run_validation(self.initial_data)
            except ValueError as exc:
                self._validated_data = {}
                self._errors.append(exc)
            else:
                self._errors = []

        if self._errors and raise_exception:
            raise ValueError(self._errors)

        return not bool(self._errors)

    def run_validation(self, initial_data):
        validators = self.get_validators()
        for attr_name in initial_data:
            if hasattr(validators, attr_name):
                try:
                    validators[attr_name](initial_data[attr_name])
                except ValueError as e:
                    self._errors.append(e)

        try:
            self._validated_data = self.validate(initial_data)
        except ValueError as e:
            self._errors.append(e)

        return not bool(self._errors)

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
            for field in self.get_fields():
                extra_kwargs = self.get_extra_kwargs_of(field)
                if extra_kwargs.get('write_only'):
                    continue

                attr = getattr(instance, field)
                ret[field] = attr
        except ValueError as e:
            self._errors.append(e)

        schema = Schema.from_dict(self._fields)()

        return schema.dump(ret)

    @property
    def data(self):
        return self.to_representation(self.instance)


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
