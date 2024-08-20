import subprocess
import pyautogui
import asyncio
from rich.console import Console
from worker_automate_hub.utils.logger import logger

console = Console()

async def conexao_rdp(task):
    try:
        ip = task["configEntrada"].get("ip", "")
        user = task["configEntrada"].get("user", "")
        password = task["configEntrada"].get("password", "")

        subprocess.Popen('mstsc')
        await asyncio.sleep(2)

        pyautogui.write(ip)
        pyautogui.press('enter')
        await asyncio.sleep(3)

        pyautogui.write(user)
        pyautogui.press('enter')
        await asyncio.sleep(2)

        pyautogui.write(password)
        pyautogui.press('enter')

        await asyncio.sleep(5)

        pyautogui.press('left')
        pyautogui.press('enter')

        await asyncio.sleep(5)

        return {"sucesso": True, "retorno": "Processo de conexão ao RDP executado com sucesso."}

    except Exception as ex:
        err_msg = f"Erro ao executar conexao_rdp: {ex}"
        logger.error(err_msg)
        console.print(err_msg, style="bold red")
        return {"sucesso": False, "retorno": err_msg}
