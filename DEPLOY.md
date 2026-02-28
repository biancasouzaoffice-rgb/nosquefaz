# Deploy online

## Render
1. Acesse https://render.com e clique em `New +` -> `Blueprint`.
2. Conecte o repositório `biancasouzaoffice-rgb/nosquefaz`.
3. Confirme o serviço `nosquefaz` detectado pelo arquivo `render.yaml`.
4. Clique em `Apply`.
5. Ao finalizar o build, abra a URL gerada (`https://...onrender.com`).

## Railway
1. Acesse https://railway.app e clique em `New Project`.
2. Selecione `Deploy from GitHub repo`.
3. Escolha o repositório `biancasouzaoffice-rgb/nosquefaz`.
4. O Railway vai usar `railway.json` e iniciar com:
   `gunicorn app:app`.
5. Em `Settings` -> `Networking`, gere o domínio público.
