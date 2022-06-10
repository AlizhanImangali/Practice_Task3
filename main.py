package main

import (
	"database/sql"
	"encoding/json"

	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	_ "github.com/lib/pq"
)

type User struct {
	id         int    `json:"id"`
	User_id    int    `json:"user_id"`
	First_name string `json:"first_name"`
	Last_name  string `json:"last_name"`
	Biin       string `json:"biin"`
	Email      string `json:"email"`
	Phone      string `json:"phone"`
	Passwrd    string `json:"passwrd"`
}
type JsonResponse struct {
	Type    string `json:"type"`
	Success bool   `json:"success"`
	Message string `json:"message"`
}

const (
	DB_USER     = "postgres"
	DB_PASSWORD = "1234"
	DB_NAME     = "test"
)

func main() {
	// Init the mux router
	router := mux.NewRouter()

	// Route handles & endpoints

	// Get user by biin
	router.HandleFunc("/user/{biin}", GetUser2).Methods("GET")

	// Create a user
	router.HandleFunc("/user", CreateUser).Methods("POST")
	router.HandleFunc("/user/updatePhone", updatePhone).Methods("PUT")
	// serve the app
	//PerformPostJsonRequest()
	fmt.Println("Server at 8000")
	log.Fatal(http.ListenAndServe(":8000", router))

}
func checkErr(err error) {
	if err != nil {
		panic(err)
	}
}

func DB() *sql.DB {
	connStr := "user=postgres password=1234 dbname=Test sslmode=disable"
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		panic(err)
	}
	//defer db.Close()
	return db
}

func updatePhone(w http.ResponseWriter, r *http.Request) {
	db := DB()
	user := User{}
	user.Biin = "5"
	user.Phone = "1231456"
	defer db.Close()
	_, err := db.Exec("UPDATE S_Users SET phone=$2 where biin= $1;", user.Biin, user.Phone)
	if err != nil {
		http.Error(w, http.StatusText(500), http.StatusInternalServerError)
		return
	}
	fmt.Fprintf(w, "User updated\n")
	response := JsonResponse{Type: "success", Success: true, Message: "The user changed successfully!"}

	json.NewEncoder(w).Encode(response)

}
