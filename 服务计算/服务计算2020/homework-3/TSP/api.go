package main

import (
	"encoding/json"
	"github.com/gorilla/handlers"
	"github.com/gorilla/mux"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"
)

type result struct {
	Id       int   `json:"id"`
	Path     []int `json:"path"`
	Distance uint  `json:"distance"`
}
type dstMapType struct {
	Id     int      `json:"id"`
	DstMap [][]uint `json:"dst_map"`
	N      int      `json:"n"`
	info   [][]uint
}

var resultMap map[int]result
var index = 0

func uploadMap(w http.ResponseWriter, r *http.Request) {
	reqBody, _ := ioutil.ReadAll(r.Body)
	var dstMap dstMapType
	_ = json.Unmarshal(reqBody, &dstMap)
	dstMap.Id = index
	go Run(&dstMap)
	index++
	_ = json.NewEncoder(w).Encode(dstMap)
}
func getResult(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(mux.Vars(r)["id"])
	for i := 0; i < 50; i++ {
		if val, ok := resultMap[id]; ok {
			_ = json.NewEncoder(w).Encode(val)
			return
		}
		time.Sleep(10 * time.Millisecond)
	}
	http.NotFoundHandler().ServeHTTP(w, r)
}

func handleRequests() {
	myRouter := mux.NewRouter().StrictSlash(true)
	myRouter.HandleFunc("/map", uploadMap).Methods("POST")
	myRouter.HandleFunc("/result/{id}", getResult).Methods("GET")
	log.Fatal(http.ListenAndServe(":10000", handlers.LoggingHandler(os.Stdout, myRouter)))
}

func main() {
	resultMap = make(map[int]result)
	handleRequests()
}
