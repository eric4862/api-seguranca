from marshmallow import Schema, fields, validates, ValidationError
import re

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    nome = fields.Str(required=True)
    senha = fields.Str(required=True, load_only=True)

    @validates('nome')
    def validate_nome(self, value):
        if not value.strip():
            raise ValidationError('O nome não pode ser vazio.')

    @validates('senha')
    def validate_senha(self, value):
        if len(value) < 8:
            raise ValidationError('A senha deve ter pelo menos 8 caracteres.')
        if not re.search(r'\d', value):
            raise ValidationError('A senha deve conter ao menos um número.')
        if not re.search(r'[A-Z]', value):
            raise ValidationError('A senha deve conter ao menos uma letra maiúscula.')
        if not re.search(r'[a-z]', value):
            raise ValidationError('A senha deve conter ao menos uma letra minúscula.')
        if not re.search(r'[@!%*?&]', value):
            raise ValidationError('A senha deve conter ao menos um caractere especial (@, !, %, *, ?, &).')

class MensagemSchema(Schema):
    id = fields.Int(dump_only=True)
    conteudo = fields.Str(required=True)
    data_hora = fields.DateTime(dump_only=True)
    autor = fields.Int(required=True, dump_only=True)
