from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
from time import sleep
from random import randint

# Carregar variáveis de ambiente
load_dotenv()

# Obter credenciais do .env
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

if not USERNAME or not PASSWORD:
    raise ValueError(
        "Por favor, configure as variáveis USERNAME e PASSWORD no arquivo .env")


def login_instagram(driver, username, password):
    """Realiza login no Instagram."""
    driver.get('https://www.instagram.com/accounts/login/')
    sleep(randint(5, 10))  # Pausa aleatória

    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    sleep(randint(5, 10))  # Outra pausa aleatória


def handle_save_login_info(driver, username):
    """Descarta a mensagem para salvar informações de login e redireciona para o perfil do usuário."""
    try:
        skip_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[text()="Agora não"]'))
        )
        skip_button.click()
        print("Mensagem para salvar informações descartada.")

        driver.get(f'https://www.instagram.com/{username}/')
        sleep(randint(5, 10))  # Pausa para carregar o perfil

    except Exception as e:
        print(
            f"Erro ao descartar mensagem de salvar informações ou redirecionar: {e}")


def open_following_modal(driver, username):
    """Abre o modal de 'Seguindo' na página do usuário."""
    try:
        driver.get(f'https://www.instagram.com/{username}/following/')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="dialog"]'))
        )
        print("Modal 'Seguindo' aberto com sucesso.")
    except Exception as e:
        print(f"Erro ao abrir o modal 'Seguindo': {e}")


def scroll_modal(driver):
    """Rola o modal para carregar todos os perfis."""
    try:
        modal = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@role="dialog"]//div[contains(@class, "x9f619")]'))
        )
        last_height = driver.execute_script(
            "return arguments[0].scrollHeight", modal)
        while True:
            driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            sleep(randint(2, 4))
            new_height = driver.execute_script(
                "return arguments[0].scrollHeight", modal)
            if new_height == last_height:
                break
            last_height = new_height
        print("Modal carregado completamente.")
    except Exception as e:
        print(f"Erro ao rolar o modal: {e}")


def close_blocking_elements(driver):
    """Fecha elementos bloqueadores como pop-ups ou mensagens."""
    try:
        blocking_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(@class, "x1qjc9v5")]'))
        )
        driver.execute_script(
            "arguments[0].style.visibility='hidden';", blocking_element)
        print("Elemento bloqueador ocultado.")
    except:
        print("Nenhum elemento bloqueador encontrado.")


def safe_click(driver, element, retries=3):
    """Tenta clicar em um elemento várias vezes."""
    for attempt in range(retries):
        try:
            element.click()
            return
        except Exception as e:
            print(f"Tentativa {attempt + 1} falhou: {e}")
            sleep(2)
    raise Exception(
        "Não foi possível clicar no elemento após várias tentativas.")


def unfollow_profiles_in_modal(driver, max_unfollows, session_limit, pause_duration):
    """Interage com o modal e remove perfis seguindo."""
    try:
        unfollow_count = 0
        while unfollow_count < max_unfollows:
            for _ in range(session_limit):
                if unfollow_count >= max_unfollows:
                    break

                # Localizar o botão "Seguindo"
                unfollow_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//button[.//div[text()="Seguindo"]]'))
                )

                # Rolagem para o botão para evitar sobreposição
                driver.execute_script(
                    "arguments[0].scrollIntoView(true);", unfollow_button)

                # Fechar elementos bloqueadores
                close_blocking_elements(driver)

                # Clicar no botão com segurança
                safe_click(driver, unfollow_button)
                sleep(randint(2, 5))

                # Confirmar "Deixar de seguir"
                confirm_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//button[text()="Deixar de seguir"]'))
                )
                safe_click(driver, confirm_button)
                sleep(randint(5, 10))

                unfollow_count += 1
                print(f"Perfis removidos: {unfollow_count}")

            # Pausar após a sessão
            print(
                f"Concluída uma sessão de {session_limit} perfis. Pausando por {pause_duration} minutos...")
            sleep(pause_duration * 60)

        print(
            f"Processo concluído. Total de perfis removidos: {unfollow_count}")
    except Exception as e:
        print(f"Erro ao deixar de seguir: {e}")


# Configurações do usuário
MAX_UNFOLLOWS = 3000  # Número total de perfis para parar de seguir
SESSION_LIMIT = 100   # Número de perfis por sessão
PAUSE_DURATION = 10   # Pausa entre sessões em minutos

# Configuração do WebDriver
driver = webdriver.Chrome()

try:
    login_instagram(driver, USERNAME, PASSWORD)
    handle_save_login_info(driver, USERNAME)
    open_following_modal(driver, USERNAME)
    scroll_modal(driver)
    unfollow_profiles_in_modal(
        driver, MAX_UNFOLLOWS, SESSION_LIMIT, PAUSE_DURATION)
finally:
    driver.quit()
