# === FURIA CS:GO BOT - FINAL ===
# Desenvolvido com carinho por um fã da FURIA 🐾

import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# === CONFIGURAÇÕES ===
TOKEN = "7856529738:AAGgHJh7nBaSR1jPdrW7JcIeaYB1mAURKU0"
SPREADSHEET_ID = "1R8FXpYPO8jCgrwKbcf5IASYHf10Rwmjw03pN2tYAEgE"


SHEET_NAMES = {
    'elenco': "Elenco Atual",
    'jogos': "Partidas",
    'estatisticas': "Estatísticas",
    'transferencias': "Transferências",
    'torneios': "Torneios",
    'ranking': "Ranking",
    'redes': "Redes"
}

EMOJIS = {
    "pantera": "🐾",
    "menu": "🏠",
    "voltar": "🔙",
    "time": "👥",
    "calendario": "📅",
    "stats": "📊",
    "transfer": "🔄",
    "torneio": "🏆",
    "ranking": "🏅",
    "rede": "🌐",
    "torcida": "🎤"
}

planilha_cache = {}

# === FUNÇÕES DE INTERFACE ===
def create_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{EMOJIS['time']} Elenco", callback_data='elenco'),
         InlineKeyboardButton(f"{EMOJIS['calendario']} Jogos", callback_data='jogos')],
        [InlineKeyboardButton(f"{EMOJIS['stats']} Estatísticas", callback_data='estatisticas'),
         InlineKeyboardButton(f"{EMOJIS['transfer']} Transferências", callback_data='transferencias')],
        [InlineKeyboardButton(f"{EMOJIS['torneio']} Torneios", callback_data='torneios'),
         InlineKeyboardButton(f"{EMOJIS['ranking']} Ranking", callback_data='ranking')],
        [InlineKeyboardButton(f"{EMOJIS['rede']} Redes Sociais", callback_data='redes')],
        [InlineKeyboardButton(f"{EMOJIS['torcida']} Torcida FURIA", callback_data='torcida')]
    ])

def create_back_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{EMOJIS['voltar']} Voltar ao Menu", callback_data='menu')]
    ])

# === FUNÇÃO PARA CARREGAR A PLANILHA ===
def carregar_planilha():
    global planilha_cache
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'credentials.json', ['https://www.googleapis.com/auth/spreadsheets']
    )
    client = gspread.authorize(creds)
    try:
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        for key, aba in SHEET_NAMES.items():
            worksheet = spreadsheet.worksheet(aba)
            planilha_cache[key] = worksheet.get_all_records()
    except Exception as e:
        logging.error(f"Erro ao carregar planilha: {e}")
        planilha_cache.clear()

# === FORMATAR CONTEÚDO DA PLANILHA ===
def formatar_conteudo_planilha(chave):
    conteudo = planilha_cache.get(chave, [])
    if not conteudo:
        return "Nenhuma informação encontrada."

    texto = f"*{SHEET_NAMES[chave]}*\n\n"
    for linha in conteudo:
        for k, v in linha.items():
            texto += f"*{k}:* {v}\n"
        texto += "\n"
    return texto

# === COMANDOS DE TEXTO ===
async def comandos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/ultimosresultados - Veja os últimos jogos\n"
        "/estatisticasjogadores - Estatísticas recentes\n"
        "/transferenciasrecentes - Mudanças no elenco\n"
        "/rankingatual - Ranking global da equipe\n"
        "/historiafuria - Conheça a trajetória da FURIA",
        parse_mode='Markdown'
    )

async def ultimos_resultados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(formatar_conteudo_planilha('jogos'), parse_mode='Markdown')

async def estatisticas_jogadores(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(formatar_conteudo_planilha('estatisticas'), parse_mode='Markdown')

async def transferencias_recentes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(formatar_conteudo_planilha('transferencias'), parse_mode='Markdown')

async def ranking_atual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(formatar_conteudo_planilha('ranking'), parse_mode='Markdown')

async def historia_furia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "A FURIA foi fundada em 2017 com o objetivo de se tornar uma das maiores equipes do mundo no CS:GO. "
        "Desde então, acumulou fãs apaixonados, títulos expressivos e uma identidade marcante! 🚀",
        parse_mode='Markdown'
    )

# === MOSTRAR MENU PRINCIPAL ===
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        f"{EMOJIS['pantera']} *Bem-vindo ao Bot da FURIA!*\n\n"
        "Você pode usar os botões abaixo ou digitar comandos como:\n"
        "📅 /ultimosresultados\n"
        "📊 /estatisticasjogadores\n"
        "🔄 /transferenciasrecentes\n"
        "🏅 /rankingatual\n"
        "📜 /historiafuria\n\n"
        "Para ver a lista completa, digite /comandos. 🧠"
    )

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=texto,
            reply_markup=create_main_menu(),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            text=texto,
            reply_markup=create_main_menu(),
            parse_mode='Markdown'
        )

# === START ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu(update, context)

# === CALLBACK DOS BOTÕES ===
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'menu':
        await show_main_menu(update, context)
        return

    if data == 'torcida':
        await query.edit_message_text(
            text="Torcida que empurra com garra! 💥\nSiga a FURIA nas redes sociais e acompanhe ao vivo os jogos da equipe!",
            reply_markup=create_back_button()
        )
        return

    if data in planilha_cache:
        mensagem = formatar_conteudo_planilha(data)
        await query.edit_message_text(
            text=mensagem,
            reply_markup=create_back_button(),
            parse_mode='Markdown'
        )

# === MAIN ===
def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    carregar_planilha()

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('comandos', comandos))
    application.add_handler(CommandHandler('ultimosresultados', ultimos_resultados))
    application.add_handler(CommandHandler('estatisticasjogadores', estatisticas_jogadores))
    application.add_handler(CommandHandler('transferenciasrecentes', transferencias_recentes))
    application.add_handler(CommandHandler('rankingatual', ranking_atual))
    application.add_handler(CommandHandler('historiafuria', historia_furia))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling()

if __name__ == '__main__':
    main()