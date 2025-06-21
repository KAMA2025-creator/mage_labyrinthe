import socket
import subprocess
import re
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Fonction principale pour lancer le scan
def lancer_scan():
    domaine = entry_domaine.get().strip()
    if domaine.lower() == "exit":
        root.destroy()
        return

    if not domaine:
        messagebox.showwarning("Attention", "Veuillez saisir un nom de domaine.")
        return

    resultat_final = []
    try:
        ip = socket.gethostbyname(domaine)
        resultat_final.append(f"L'adresse IP de {domaine} est : {ip}")

        # PING
        reussites = 0
        for _ in range(3):
            res = subprocess.run(["ping", "-n", "1", ip], stdout=subprocess.DEVNULL)
            if res.returncode == 0:
                reussites += 1
        pourcentage = (reussites / 3) * 100
        resultat_final.append(f"{reussites}/3 pings réussis ({pourcentage:.0f}%)")
        if reussites == 0:
            resultat_final.append("Aucune réponse au ping (peut être bloqué par un pare-feu)")

        # TTL
        res = subprocess.run(["ping", "-n", "1", ip], capture_output=True, text=True)
        texte_ping = res.stdout
        match = re.search(r"TTL=(\d+)", texte_ping, re.IGNORECASE)
        if match:
            ttl = int(match.group(1))
            resultat_final.append(f"TTL reçu : {ttl}")
            if 0 < ttl <= 64:
                resultat_final.append("Probablement Linux")
            elif 65 <= ttl <= 128:
                resultat_final.append("Probablement Windows")
            elif ttl > 128:
                resultat_final.append("Probablement Cisco ou équipement réseau")
            else:
                resultat_final.append("Impossible de deviner le système")

        # Résolution inverse
        try:
            nom_machine = socket.gethostbyaddr(ip)[0]
            resultat_final.append(f"Résolution inverse : {ip} → {nom_machine}")
        except socket.herror:
            resultat_final.append("Aucun nom associé à cette adresse IP.")

        # Bannières
        def lire_banniere(ip, port):
            try:
                prise = socket.socket()
                prise.settimeout(2)
                prise.connect((ip, port))
                banniere = prise.recv(1024).decode(errors="ignore")
                prise.close()
                return banniere.strip()
            except:
                return "Pas de bannière ou non lisible"

        # Scan ports
        ports = [22, 80, 443, 3306]
        ports_ouverts = []
        resultat_final.append("Scan des ports en cours...")
        for port in ports:
            prise = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            prise.settimeout(1)
            result = prise.connect_ex((ip, port))
            if result == 0:
                ports_ouverts.append(port)
                resultat_final.append(f"Port {port} ouvert")
                banniere = lire_banniere(ip, port)
                resultat_final.append(f"  → {banniere}")
            else:
                resultat_final.append(f"Port {port} fermé")
            prise.close()

        # Requête HTTP
        def requete_http(domaine):
            try:
                prise = socket.socket()
                prise.settimeout(3)
                prise.connect((ip, 80))
                requete = f"GET / HTTP/1.1\r\nHost: {domaine}\r\n\r\n"
                prise.send(requete.encode())
                reponse = prise.recv(1024).decode(errors="ignore")
                prise.close()
                resultat_final.append("📝 Réponse HTTP :")
                resultat_final.append(reponse.strip())
            except:
                resultat_final.append("❌ Échec de la requête HTTP.")
        requete_http(domaine)

        # Scan sous-domaines
        def scanner_sous_domaines(domaine):
            sous_domaines = ["www", "mail", "admin", "ftp", "webmail", "dev", "vpn"]
            resultat_final.append("\n🔎 Scan des sous-domaines connus :")
            for prefixe in sous_domaines:
                sous_domaine = f"{prefixe}.{domaine}"
                try:
                    ip_sous = socket.gethostbyname(sous_domaine)
                    resultat_final.append(f"✅ {sous_domaine} → {ip_sous}")
                except socket.gaierror:
                    resultat_final.append(f"❌ {sous_domaine} introuvable")
        scanner_sous_domaines(domaine)

        # Rapport
        nom_fichier = f"rapport_{domaine.replace('.', '_')}.txt"
        with open(nom_fichier, "w", encoding="utf-8") as fichier:
            fichier.write("\n".join(resultat_final))

        # Historique
        date_scan = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ports_str = ", ".join(str(p) for p in ports_ouverts) if ports_ouverts else "aucun port ouvert"
        ligne = f"[{date_scan}] Domaine : {domaine} | IP : {ip} | Ports ouverts : {ports_str}\n"
        with open("historique.txt", "a", encoding="utf-8") as fichier:
            fichier.write(ligne)

        # ASCII ports
        etat_ports = ["■" if port in ports_ouverts else "□" for port in ports]
        ascii_ports = f"\nPorts scannés : {ports}\nÉtat          : {etat_ports}"
        resultat_final.append(ascii_ports)

        # Affichage dans la zone texte
        text_resultat.config(state='normal')
        text_resultat.delete(1.0, tk.END)
        text_resultat.insert(tk.END, "\n".join(resultat_final))
        text_resultat.config(state='disabled')

        # Messages d'info
        messagebox.showinfo("Scan terminé", f"Scan terminé ! Rapport sauvegardé sous : {nom_fichier}\nHistorique mis à jour.")

    except socket.gaierror:
        messagebox.showerror("Erreur", "Domaine invalide ou introuvable.")
        # Pas de compteur de tentatives dans l'interface graphique, on laisse simple


# Création fenêtre principale
root = tk.Tk()
root.title("CYBERSCAN PRO+")
root.geometry("700x600")

# Label et champ saisie
label = tk.Label(root, text="Entrez un nom de domaine :", font=("Arial", 14))
label.pack(pady=10)

entry_domaine = tk.Entry(root, font=("Arial", 14), width=40)
entry_domaine.pack(pady=5)
entry_domaine.focus()

# Bouton lancer scan
btn_scan = tk.Button(root, text="Lancer le scan", font=("Arial", 14), command=lancer_scan)
btn_scan.pack(pady=10)

# Zone texte pour afficher le résultat (scrollable)
text_resultat = scrolledtext.ScrolledText(root, font=("Consolas", 11), width=80, height=25, state='disabled')
text_resultat.pack(padx=10, pady=10)

# Boucle principale
root.mainloop()
