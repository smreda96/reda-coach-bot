import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN manquant dans les variables d'environnement")
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# =============================================
# INSÈRE TON TOKEN ICI
TOKEN = os.environ.get("8947406741:AAHX27qzBEVDoTfxkz68jbyW4TAifhPhY1E")
# =============================================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# KEYBOARDS
main_keyboard = ReplyKeyboardMarkup([
    ["💪 Programme", "🏃 Course"],
    ["🍽️ Nutrition", "✅ Checklist"],
    ["📋 Log séance", "📊 Mon profil"]
], resize_keyboard=True)

# PROGRAMME SALLE
programme = {
    "lundi": """
💪 *LUNDI — PUSH*
_Chest, épaules, triceps | 45-60 min_

| Exercice | Sets x Reps | RPE |
|----------|-------------|-----|
| Chest Press machine | 3 x 12 | 6-7 |
| Shoulder Press machine | 3 x 12 | 6-7 |
| Pec Dec (butterfly) | 3 x 12 | 6-7 |
| Tricep Pushdown cable | 3 x 12 | 6-7 |
| Plank | 3 x 30s | — |

⏱ Repos : 90 sec entre chaque série
🥤 Shaker whey + créatine 5g après séance
    """,
    "mercredi": """
💪 *MERCREDI — PULL + JAMBES*
_Dos, biceps, jambes | 45-60 min_

| Exercice | Sets x Reps | RPE |
|----------|-------------|-----|
| Lat Pulldown | 3 x 12 | 6-7 |
| Cable Row | 3 x 12 | 6-7 |
| Bicep Curl machine | 3 x 12 | 6-7 |
| Leg Press | 3 x 12 | 6-7 |
| Leg Curl | 3 x 12 | 6-7 |

⏱ Repos : 90 sec entre chaque série
🥤 Shaker whey + créatine 5g après séance
    """,
    "dimanche": """
💪 *DIMANCHE — FULL BODY*
_Corps complet + core | 45-60 min_

| Exercice | Sets x Reps | RPE |
|----------|-------------|-----|
| Chest Press machine | 3 x 12 | 6-7 |
| Lat Pulldown | 3 x 12 | 6-7 |
| Shoulder Press machine | 3 x 10 | 6-7 |
| Leg Press | 3 x 12 | 6-7 |
| Cable Row | 3 x 10 | 6-7 |
| Plank | 3 x 30s | — |

⏱ Repos : 90 sec entre chaque série
🥤 Shaker whey + créatine 5g après séance
    """
}

# PROGRAMME COURSE
course = {
    "mardi": """
🏃 *MARDI — COURSE FACILE*
_Zone 2 — Endurance de base_

• Distance : 6 km
• Allure : 5:30-5:45/km
• FC cible : Zone 2 (conversation possible)
• Chaussures : NB Fresh Foam 1080

⚠️ Reste en Zone 2 — résiste à l'envie d'accélérer
    """,
    "jeudi": """
🏃 *JEUDI — TEMPO*
_Séance qualité_

• Échauffement : 2 km à 5:45/km
• Blocs : 2 x 10 min à 5:10/km
• Récup : 3 min entre blocs
• Retour calme : 1-2 km
• Chaussures : NB Rebel

⚠️ Ne dépasse pas 5:10/km sur les blocs
    """,
    "samedi": """
🏃 *SAMEDI — SORTIE LONGUE*
_Endurance fondamentale_

• Distance : 12-16 km
• Allure : 5:20-5:30/km
• FC : Zone 2 strict
• Chaussures : NB Fresh Foam 1080
• Nutrition : Dattes Medjoul toutes les 20-25 min à partir du km 8

⚠️ Ton problème récurrent : tu accélères en fin de sortie — tiens l'allure jusqu'au bout
    """
}

# NUTRITION
nutrition_text = """
🍽️ *NUTRITION JOURNALIÈRE*
_Cible : 2,280 kcal | 170g protéines_

🌅 *Petit déjeuner* — 480 kcal | 32g P
4 œufs brouillés + 2 tranches pain complet + lait

🍽️ *Déjeuner (resto)* — 650 kcal | 50g P
Poulet/viande grillée + riz + salade
Sans sauce lourde — eau plutôt que jus

🍎 *Snack* — 220 kcal | 20g P
200g fromage blanc 0% + 1 banane

🌙 *Dîner* — 520 kcal | 42g P
150g thon + 80g riz + légumes

🥤 *Whey post-séance* — 120 kcal | 25g P

*Macros :*
• Protéines : 170g (priorité absolue)
• Glucides : 240g
• Lipides : 65g

💊 Créatine 5g tous les jours sans exception
"""

# CHECKLIST
checklist_text = """
✅ *CHECKLIST DU JOUR*

Coche mentalement chaque item :

☐ 💊 Créatine 5g (dans eau ou shaker)
☐ 🏋️ Séance du jour faite
☐ 🥤 Shaker whey post-séance
☐ 🍗 170g protéines atteints
☐ 💧 2-3L d'eau
☐ 😴 7-8h de sommeil

*Règle anti-démotivation :*
Ne rate jamais 2 fois de suite.
Un jour raté c'est normal.
Deux jours ratés c'est le début de l'abandon.
"""

# PROFIL
profil_text = """
👤 *PROFIL REDA*

• Âge : 26-35 ans
• Poids : 68 kg
• Taille : 180 cm
• Objectif : Recomposition (muscle + perte graisse)
• Niveau : Débutant → Intermédiaire

*Programme :* 2 mois — In Shape
*Salle :* 3x/semaine (Lun/Mer/Dim)
*Course :* 3x/semaine (Mar/Jeu/Sam)

*Suppléments :*
• Whey — post-séance
• Créatine 5g — quotidien

*Course à pied :*
• Semi-marathon : 1h47:53 (Marrakech)
• Chaussures : NB 1080 / Rebel / Elite carbone
• Nutrition course : Dattes Medjoul km 8+

*Calories :* 2,280 kcal/jour
*Protéines :* 170g/jour
"""

# HANDLERS
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💪 *Salut Reda !*\n\nJe suis ton coach personnel. Utilise les boutons ci-dessous pour accéder à ton programme.",
        parse_mode='Markdown',
        reply_markup=main_keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "programme" in text or "💪" in text:
        await update.message.reply_text(
            "💪 *PROGRAMME SALLE*\nChoisis ton jour :",
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardMarkup([
                ["Lundi", "Mercredi", "Dimanche"],
                ["⬅️ Retour"]
            ], resize_keyboard=True)
        )

    elif "course" in text or "🏃" in text:
        await update.message.reply_text(
            "🏃 *PROGRAMME COURSE*\nChoisis ton jour :",
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardMarkup([
                ["Mardi", "Jeudi", "Samedi"],
                ["⬅️ Retour"]
            ], resize_keyboard=True)
        )

    elif text in ["lundi", "mercredi", "dimanche"]:
        await update.message.reply_text(programme[text], parse_mode='Markdown', reply_markup=main_keyboard)

    elif text in ["mardi", "jeudi", "samedi"]:
        await update.message.reply_text(course[text], parse_mode='Markdown', reply_markup=main_keyboard)

    elif "nutrition" in text or "🍽️" in text:
        await update.message.reply_text(nutrition_text, parse_mode='Markdown', reply_markup=main_keyboard)

    elif "checklist" in text or "✅" in text:
        await update.message.reply_text(checklist_text, parse_mode='Markdown', reply_markup=main_keyboard)

    elif "profil" in text or "📊" in text:
        await update.message.reply_text(profil_text, parse_mode='Markdown', reply_markup=main_keyboard)

    elif "log" in text or "📋" in text:
        await update.message.reply_text(
            "📋 *LOG SÉANCE*\n\nEnvoie ton log dans ce format :\n\n`[Séance] — [Date]\nExercice | Sets x Reps | Poids | RPE | Notes`\n\nExemple :\n`Lundi PUSH — 26/05\nChest Press | 3x12 | 20kg | 6 | Trop léger`",
            parse_mode='Markdown',
            reply_markup=main_keyboard
        )

    elif "retour" in text or "⬅️" in text:
        await update.message.reply_text("Menu principal :", reply_markup=main_keyboard)

    else:
        await update.message.reply_text(
            "Utilise les boutons ou tape :\n• *programme* — salle\n• *course* — running\n• *nutrition* — macros\n• *checklist* — jour\n• *profil* — ton profil",
            parse_mode='Markdown',
            reply_markup=main_keyboard
        )

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from datetime import datetime
    days = {0: "lundi", 1: "mardi", 2: "mercredi", 3: "jeudi", 4: "vendredi", 5: "samedi", 6: "dimanche"}
    day = days[datetime.now().weekday()]

    if day in programme:
        await update.message.reply_text(f"Aujourd'hui c'est {day.capitalize()} — séance salle :\n{programme[day]}", parse_mode='Markdown', reply_markup=main_keyboard)
    elif day in course:
        await update.message.reply_text(f"Aujourd'hui c'est {day.capitalize()} — course :\n{course[day]}", parse_mode='Markdown', reply_markup=main_keyboard)
    else:
        await update.message.reply_text("😴 *Vendredi — Repos complet*\n\nRécupération active. Mange bien, dors bien. Demain c'est la sortie longue 💪", parse_mode='Markdown', reply_markup=main_keyboard)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot démarré...")
    app.run_polling()

if __name__ == '__main__':
    main()
