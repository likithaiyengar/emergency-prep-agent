import os
from groq import Groq
from dotenv import load_dotenv
from memory import save_message, get_history, get_profile, save_profile, init_db

load_dotenv()
client = Groq(api_key=os.getenv("OPENAI_API_KEY"))

CHECKLISTS = {
    'earthquake': ['Store 3L water per person per day','Keep a first aid kit','Have a torch with batteries','Save emergency contacts offline','Keep sturdy shoes near your bed','Know your building exit routes'],
    'flood': ['Pack documents in waterproof bag','Know your evacuation route','Keep a battery-powered radio','Store extra medication','Avoid walking in floodwater','Keep phone charged during warnings'],
    'fire': ['Memorize two exit routes','Agree on meeting point with roommates','Check smoke alarms monthly','Keep fire extinguisher accessible','Never overload electrical sockets','Crawl low under smoke to exit'],
    'cyclone': ['Stock food and water for 3 days','Charge all devices before cyclone','Stay indoors away from windows','Know your nearest cyclone shelter','Secure loose items outside your room']
}

EMERGENCY_NUMBERS = {
    'bangalore': 'Police: 100 | Fire: 101 | Ambulance: 108 | BBMP: 1533 | Disaster: 1070',
    'bengaluru': 'Police: 100 | Fire: 101 | Ambulance: 108 | BBMP: 1533 | Disaster: 1070',
    'mumbai': 'Police: 100 | Fire: 101 | Ambulance: 108 | Flood Helpline: 1916',
    'delhi': 'Police: 100 | Fire: 101 | Ambulance: 108 | Disaster: 1077',
    'chennai': 'Police: 100 | Fire: 101 | Ambulance: 108 | Disaster: 1070',
    'hyderabad': 'Police: 100 | Fire: 101 | Ambulance: 108 | GHMC: 040-21111111',
    'udupi': 'Police: 100 | Fire: 101 | Ambulance: 108 | Disaster: 1070',
}

def get_checklist(disaster):
    items = CHECKLISTS.get(disaster.lower(), None)
    if not items:
        return f"No checklist found for '{disaster}'. Available: earthquake, flood, fire, cyclone."
    return 'Done ' + '\nDone '.join(items)

def get_numbers(location):
    numbers = EMERGENCY_NUMBERS.get(location.lower(), 'Police: 100 | Fire: 101 | Ambulance: 108 | National Disaster: 1078')
    return f'Emergency Numbers for {location.title()}:\n{numbers}'

def reflect(history, profile):
    if len(history) < 4:
        return ''
    history_text = '\n'.join([f'{r.upper()}: {m}' for r, m in history])
    profile_text = f"Location: {profile.get('location','unknown')}, Housing: {profile.get('housing_type','unknown')}"
    prompt = f'You are reviewing an emergency preparedness conversation.\nStudent Profile: {profile_text}\nConversation:\n{history_text}\n\nIn 3 bullet points:\n1. What preparedness gaps remain?\n2. What should the assistant focus on next?\n3. Any advice to update based on new info?'
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content

def chat(student_id, user_message, conversation_history):
    save_message(student_id, 'user', user_message)
    msg_lower = user_message.lower()
    tool_response = None
    for disaster in ['earthquake', 'flood', 'fire', 'cyclone']:
        if disaster in msg_lower and any(w in msg_lower for w in ['checklist','prepare','safety','tips']):
            tool_response = get_checklist(disaster)
            break
    for city in EMERGENCY_NUMBERS.keys():
        if city in msg_lower and any(w in msg_lower for w in ['number','contact','emergency','helpline']):
            tool_response = get_numbers(city)
            break
    for city in EMERGENCY_NUMBERS.keys():
        if city in msg_lower:
            for housing in ['hostel','pg','apartment','home','flat']:
                if housing in msg_lower:
                    save_profile(student_id, city, housing)
                    break
    system_prompt = 'You are a friendly Emergency Preparedness Assistant for students in India. Help students prepare for disasters like earthquakes, floods, fires, and cyclones. Always ask for their city and housing type early to personalize advice. Be calm, clear, and practical.'
    messages = [{'role': 'system', 'content': system_prompt}]
    for role, msg in conversation_history[-8:]:
        messages.append({'role': role if role == 'user' else 'assistant', 'content': msg})
    if tool_response:
        messages.append({'role': 'user', 'content': user_message + f'\n\n[Tool Result]: {tool_response}'})
    else:
        messages.append({'role': 'user', 'content': user_message})
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=messages,
        max_tokens=500
    )
    result = response.choices[0].message.content
    save_message(student_id, 'agent', result)
    history = get_history(student_id)
    reflection_note = ''
    if len(history) > 0 and len(history) % 6 == 0:
        profile = get_profile(student_id)
        reflection_note = reflect(history, profile)
    return result, reflection_note