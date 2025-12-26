from docs import db, bcrypt, app
from docs.models import User

with app.app_context():
    # gerar senha
    hashed_pw = bcrypt.generate_password_hash("senha123")

    # criar usuário
    user = User(username="admin", email="admin@email.com", password=hashed_pw)

    # adicionar ao banco
    db.session.add(user)
    db.session.commit()

    print("Usuário admin criado com sucesso!")
