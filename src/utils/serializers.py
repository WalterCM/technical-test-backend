import peewee

from marshmallow import Schema, fields, pprint

from src import conf


class ModelSerializer:
    _validated = False
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
        fields = self.Meta.fields
        if fields == '__all__':
            fields = []
            for possible_field_name in dir(self.Meta.model):
                possible_field = getattr(self.Meta.model, possible_field_name)
                if isinstance(possible_field, peewee.Field):
                    fields.append(possible_field_name)

            fields = tuple(fields)
        return fields

    def get_extra_kwargs(self):
        return self.Meta.extra_kwargs

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

    def serialize_datetime(self, attr):
        if hasattr(conf, 'DATE_FORMAT'):
            serialized = attr.strftime(conf.DATE_FORMAT)
        else:
            serialized = attr.isoformat()

        return serialized

    def to_representation(self, instance):
        ret = {}
        try:
            for field in self.get_fields():
                attr = getattr(instance, field)
                names = [type(attr).__name__, attr.__class__.__name__]
                for name in names:
                    method_name = 'serialize_{}'.format(name)
                    if hasattr(self, method_name):
                        attr = getattr(self, method_name)(attr)
                        break
                ret[field] = attr
        except ValueError as e:
            self._errors.append(e)

        return ret

    @property
    def data(self):
        return self.to_representation(self.instance)


class ListSerializer(ModelSerializer):
    def __init__(self, instance=None, data=None, **kwargs):
        super().__init__(instance, data, **kwargs)

    def to_representation(self, data):
        if not type(data).__name__ == 'ModelSelect':
            raise ValueError('You need to pass a peewee queryset as instance')

        thingy = []
        for item in data:
            i = super().to_representation(item)
            thingy.append(i)
        return thingy
