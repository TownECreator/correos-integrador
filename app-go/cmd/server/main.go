package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"sync"
	"time"
)

type AuthUser struct {
	Valid    bool   `json:"valid"`
	UserID   string `json:"user_id"`
	Username string `json:"username"`
	Role     string `json:"role"`
}

type Mail struct {
	ID        int    `json:"id"`
	Sender    string `json:"sender"`
	Recipient string `json:"recipient"`
	Subject   string `json:"subject"`
	Body      string `json:"body"`
	CreatedAt string `json:"created_at"`
}

type SendMailRequest struct {
	Recipient string `json:"recipient"`
	Subject   string `json:"subject"`
	Body      string `json:"body"`
}

var (
	mails  []Mail
	nextID = 1
	mu     sync.Mutex
)

func authenticate(r *http.Request) (*AuthUser, int, string) {
	authHeader := r.Header.Get("Authorization")
	if authHeader == "" || !strings.HasPrefix(authHeader, "Bearer ") {
		return nil, http.StatusUnauthorized, "Token faltante o mal formado"
	}

	req, err := http.NewRequest("GET", "http://localhost:8000/verify", nil)
	if err != nil {
		return nil, http.StatusInternalServerError, "Error interno validando token"
	}
	req.Header.Set("Authorization", authHeader)

	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Do(req)
	if err != nil {
		return nil, http.StatusBadGateway, "No se pudo contactar al servicio de autenticación"
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, http.StatusUnauthorized, "Token inválido o expirado"
	}

	var user AuthUser
	if err := json.NewDecoder(resp.Body).Decode(&user); err != nil || !user.Valid {
		return nil, http.StatusUnauthorized, "Respuesta de autenticación inválida"
	}

	return &user, http.StatusOK, ""
}

func writeJSON(w http.ResponseWriter, status int, payload any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(payload)
}

func sendMailHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"detail": "Método no permitido"})
		return
	}

	user, status, msg := authenticate(r)
	if user == nil {
		writeJSON(w, status, map[string]string{"detail": msg})
		return
	}

	var req SendMailRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"detail": "JSON mal formado"})
		return
	}

	req.Recipient = strings.TrimSpace(req.Recipient)
	req.Subject = strings.TrimSpace(req.Subject)
	req.Body = strings.TrimSpace(req.Body)

	if req.Recipient == "" || req.Subject == "" || req.Body == "" || len(req.Subject) > 120 || len(req.Body) > 2000 {
		writeJSON(w, http.StatusBadRequest, map[string]string{"detail": "Datos inválidos: campos vacíos o longitud excedida"})
		return
	}

	mu.Lock()
	mail := Mail{
		ID:        nextID,
		Sender:    user.Username,
		Recipient: req.Recipient,
		Subject:   req.Subject,
		Body:      req.Body,
		CreatedAt: time.Now().UTC().Format(time.RFC3339),
	}
	nextID++
	mails = append(mails, mail)
	mu.Unlock()

	writeJSON(w, http.StatusCreated, map[string]any{
		"message": "Correo enviado correctamente",
		"mail":    mail,
	})
}

func mailboxHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		writeJSON(w, http.StatusMethodNotAllowed, map[string]string{"detail": "Método no permitido"})
		return
	}

	user, status, msg := authenticate(r)
	if user == nil {
		writeJSON(w, status, map[string]string{"detail": msg})
		return
	}

	owner := strings.TrimPrefix(r.URL.Path, "/mailbox/")
	owner = strings.TrimSpace(owner)
	if owner == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"detail": "Debe especificar el usuario del buzón"})
		return
	}

	if user.Username != owner && user.Role != "Admin" {
		writeJSON(w, http.StatusForbidden, map[string]string{
			"detail": fmt.Sprintf("Acceso denegado: %s no tiene permiso para leer el buzón de %s", user.Username, owner),
		})
		return
	}

	mu.Lock()
	var inbox []Mail
	for _, m := range mails {
		if m.Recipient == owner {
			inbox = append(inbox, m)
		}
	}
	mu.Unlock()

	if inbox == nil {
		inbox = []Mail{}
	}

	writeJSON(w, http.StatusOK, map[string]any{
		"mailbox": owner,
		"count":   len(inbox),
		"mails":   inbox,
	})
}

func main() {
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, http.StatusOK, map[string]string{"status": "ok", "service": "mail-go"})
	})
	http.HandleFunc("/mails/send", sendMailHandler)
	http.HandleFunc("/mailbox/", mailboxHandler)

	fmt.Println("Servidor de correo en Go escuchando en http://0.0.0.0:8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Println("Error al iniciar servidor:", err)
	}
}
