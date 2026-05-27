from backend.database import SessionLocal
from backend.models.usuario import Usuario


# ---------------------------------
# CREATE - Criar usuário
# ---------------------------------
def criar_usuario(dados):
    db = SessionLocal()

    # verifica se email já existe
    existe = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if existe:
        db.close()
        return None

    # cria usuário
    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha=dados.senha
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    db.close()

    return usuario


# ---------------------------------
# READ - Listar usuários
# ---------------------------------
def listar_usuarios():
    db = SessionLocal()

    usuarios = db.query(Usuario).all()

    resultado = [
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "animais": [
                {
                    "id": a.id,
                    "nome_popular": a.nome_popular
                }
                for a in u.animais
            ] if hasattr(u, "animais") else []
        }
        for u in usuarios
    ]

    db.close()
    return resultado


# ---------------------------------
# READ - Buscar usuário por ID
# ---------------------------------
def buscar_usuario(usuario_id):
    db = SessionLocal()

    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if not usuario:
        db.close()
        return None

    resultado = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "animais": [
            {
                "id": a.id,
                "nome_popular": a.nome_popular
            }
            for a in usuario.animais
        ] if hasattr(usuario, "animais") else []
    }

    db.close()
    return resultado


# ---------------------------------
# UPDATE - Atualizar usuário
# ---------------------------------
def atualizar_usuario(usuario_id, dados):
    db = SessionLocal()

    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if not usuario:
        db.close()
        return None

    # verifica email duplicado
    if dados.email:
        email_existente = db.query(Usuario).filter(
            Usuario.email == dados.email,
            Usuario.id != usuario_id
        ).first()

        if email_existente:
            db.close()
            return "email_duplicado"

    # atualiza campos apenas se vierem no request
    if dados.nome:
        usuario.nome = dados.nome

    if dados.email:
        usuario.email = dados.email

    if dados.senha:
        usuario.senha = dados.senha

    db.commit()
    db.refresh(usuario)
    db.close()

    return usuario


# ---------------------------------
# DELETE - Remover usuário
# ---------------------------------
def deletar_usuario(usuario_id):
    db = SessionLocal()

    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if not usuario:
        db.close()
        return False

    db.delete(usuario)
    db.commit()
    db.close()

    return True