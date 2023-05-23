import requests

def function_name(request):
    # URL de tu Cloud Run
    url = 'https://build-workflows-55nsgsicwq-uc.a.run.app'

    # Realiza la petición a Cloud Run
    response = requests.get(url)
    print(response)

    # Verifica el código de estado de la respuesta
    if response.status_code == 200:
        return 'Petición exitosa'
    else:
        return 'Error en la petición'
