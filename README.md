-Crear un archivo cookies.json y colocar las cookies de chatgpt obtenidas con la extension EditThisCookie

-Crear un archivo chatHistory.json y colocar el object response del endpoint:
backend-api/conversations
El cual aparece al cargar la pagina del chatgpt

-Para crear en entorno virtual:
python -m venv env 

-Para cargar el entorno virtual:
call env/scripts/activate

-Instalar las dependencias:
pip install -r requirements.txt

-Ejecutar la aplicacion:
flask --app app.py --debug run --host=192.168.0.101

-Al ejecutar se abren dos chrome, cerrar el primero una vez que esten los dos abiertos


