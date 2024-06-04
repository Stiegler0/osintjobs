import streamlit as st
import json
import os

def gen_email(domain, full_name, pattern):
    full_name = full_name.strip()
    name_parts = full_name.split()
    first_name = name_parts[0].lower()
    last_name = name_parts[-1].lower()
    email = pattern
    email = email.replace("{first}", first_name)
    email = email.replace("{f}", first_name[0])
    email = email.replace("{last}", last_name)
    email += domain
    return email

def extract_company_name(domain):
    company_name = domain.split('@')[1].split('.')[0]
    return company_name

def save_args(file_path, arguments):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            history = json.load(file)
    else:
        history = []

    history.append(arguments)

    with open(file_path, "w") as file:
        json.dump(history, file, indent=4)

def load_history(file_path):
    with open(file_path, 'r') as file:
        history = json.load(file)
    return history

def main():
    st.title('Generate Email Address')

    domain = st.text_input('Enter the domain for the email address, e.g., @lesechosleparisien.fr')
    full_name = st.text_input('Enter the full name of the user, e.g., Yassine Jemlaoui')
    pattern = st.text_input('Enter the pattern for the email, e.g., {first}.{last}@...')

    if st.button('Generate Email'):
        if domain and full_name and pattern:
            company_name = extract_company_name(domain)
            email = gen_email(domain, full_name, pattern)

            st.write(f"Generated Email: {email}")

            # Save arguments to history
            args_dict = {'domain': domain, 'full_name': full_name, 'pattern': pattern, 'company_name': company_name}
            history_file = 'arguments.json'
            save_args(history_file, args_dict)
        else:
            st.warning('Please fill in all fields.')

    history_file = 'arguments.json'
    history = load_history(history_file)
    
    if not history:
        st.sidebar.write('L\'historique est vide.')
    else:
        options = st.sidebar.multiselect(
            "Quelles options souhaitez-vous extraire ?",
            ["Domaine", "Nom Complet", "Pattern", "Nom de l'entreprise"],
            ["Nom de l'entreprise"]
        )

        st.sidebar.write('Historique des Arguments :')
        for idx, entry in enumerate(history, 1):
            st.sidebar.write(f"**Entrée {idx}:**")
            for option in options:
                if option == "Domaine":
                    st.sidebar.write(f"Domaine: {entry['domain']}")
                elif option == "Nom Complet":
                    st.sidebar.write(f"Nom Complet: {entry['full_name']}")
                elif option == "Pattern":
                    st.sidebar.write(f"Pattern: {entry['pattern']}")
                elif option == "Nom de l'entreprise":
                    st.sidebar.write(f"Nom de l'entreprise: {entry['company_name']}")
            st.sidebar.write('---')

if __name__ == "__main__":
    main()