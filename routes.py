from flask import Blueprint, request, jsonify
from models import db, Usuario, Mensagem
from schemas import UsuarioSchema, MensagemSchema

routes = Blueprint('routes', __name__)
usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
mensagem_schema = MensagemSchema()
mensagens_schema = MensagemSchema(many=True)

# CRUD Usuário
@routes.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.json
    errors = usuario_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    novo_usuario = Usuario(
        email=data['email'],
        nome=data['nome'],
        senha=data['senha']  # Importante: em produção deve-se criptografar
    )
    try:
        db.session.add(novo_usuario)
        db.session.commit()
        return usuario_schema.jsonify(novo_usuario), 201
    except Exception as e:
        return jsonify({'erro': 'Email já cadastrado ou outro problema.'}), 400

@routes.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return usuarios_schema.jsonify(usuarios)

@routes.route('/usuarios/<int:id>', methods=['GET'])
def obter_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    return usuario_schema.jsonify(usuario)

@routes.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    data = request.json
    errors = usuario_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    if 'email' in data:
        usuario.email = data['email']
    if 'nome' in data:
        usuario.nome = data['nome']
    if 'senha' in data:
        usuario.senha = data['senha']

    db.session.commit()
    return usuario_schema.jsonify(usuario)

@routes.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário deletado com sucesso.'})

# CRUD Mensagem
@routes.route('/mensagens', methods=['POST'])
def criar_mensagem():
    data = request.json
    conteudo = data.get('conteudo')
    if not conteudo:
        return jsonify({'erro': 'Conteúdo da mensagem é obrigatório.'}), 400

    nova_mensagem = Mensagem(
        conteudo=conteudo,
        autor=1  # Vinculando sempre ao usuário padrão id=1
    )
    db.session.add(nova_mensagem)
    db.session.commit()
    return mensagem_schema.jsonify(nova_mensagem), 201

@routes.route('/mensagens', methods=['GET'])
def listar_mensagens():
    mensagens = Mensagem.query.all()
    return mensagens_schema.jsonify(mensagens)

@routes.route('/mensagens/<int:id>', methods=['GET'])
def obter_mensagem(id):
    mensagem = Mensagem.query.get_or_404(id)
    return mensagem_schema.jsonify(mensagem)

@routes.route('/mensagens/<int:id>', methods=['PUT'])
def atualizar_mensagem(id):
    mensagem = Mensagem.query.get_or_404(id)
    data = request.json

    if 'autor' in data and data['autor'] != mensagem.autor:
        return jsonify({'erro': 'Não é permitido alterar o autor da mensagem.'}), 400

    if 'conteudo' in data:
        mensagem.conteudo = data['conteudo']

    db.session.commit()
    return mensagem_schema.jsonify(mensagem)

@routes.route('/mensagens/<int:id>', methods=['DELETE'])
def deletar_mensagem(id):
    mensagem = Mensagem.query.get_or_404(id)
    db.session.delete(mensagem)
    db.session.commit()
    return jsonify({'mensagem': 'Mensagem deletada com sucesso.'})
