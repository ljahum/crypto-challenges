package main

import (
	"bufio"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"net/http"
	"os/exec"
)

type User struct {
	gorm.Model
	Id       int `gorm:"primaryKey"`
	UserName string
	Password string
	Token    string
}

var db *gorm.DB

func main() {
	r := gin.Default()
	CollectRouters(r)
	panic(r.Run(":8088"))
}

func init() {
	db, _ = gorm.Open(sqlite.Open("gorm.db"), &gorm.Config{})
	db.AutoMigrate(&User{})
}

func CollectRouters(router *gin.Engine) {
	router.POST("register", register)
	router.POST("login", login)
	router.POST("client", sqlClient)
}

func register(c *gin.Context) {
	username := c.PostForm("username")
	password := c.PostForm("password")

	user := &User{}
	db.Where("user_name", username).First(user)
	if user.UserName == username {
		c.JSON(http.StatusInternalServerError, gin.H{"msg": "用户名已被注册"})
		return
	}

	token := randomUUID()
	db.Create(&User{
		UserName: username,
		Password: password,
		Token:    token,
	})
	c.JSON(http.StatusOK, gin.H{"msg": "注册成功", "token": token})
}

func login(c *gin.Context) {
	username := c.PostForm("username")
	password := c.PostForm("password")
	token := c.PostForm("token")

	user := &User{}
	err := db.Where(&User{UserName: username, Password: password, Token: token}).First(&user).Error
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"msg": "登录失败"})
		return
	}
	c.JSON(http.StatusOK, gin.H{"msg": "登录成功", "user": user})
}

type ClientBody struct {
	Token string   `json:"token"`
	Sql   []string `json:"sql"`
}

func sqlClient(c *gin.Context) {
	clientBody := ClientBody{}
	c.BindJSON(&clientBody)

	user := &User{}
	db.Where("user_name = ?", "admin").First(user)
	result := ""
	if clientBody.Token == user.Token {
		println("success")

		cmd := exec.Command("sqlite3")

		stdin, err := cmd.StdinPipe()
		if err != nil {
			fmt.Println(err)
			return
		}

		stdout, err := cmd.StdoutPipe()
		if err != nil {
			fmt.Println(err)
			return
		}

		stderr, err := cmd.StderrPipe()
		if err != nil {
			fmt.Println(err)
			return
		}

		err = cmd.Start()
		if err != nil {
			fmt.Println(err)
			return
		}

		go func() {
			scanner := bufio.NewScanner(stdout)
			for scanner.Scan() {
				fmt.Println(scanner.Text())
			}
		}()

		go func() {
			scanner := bufio.NewScanner(stderr)
			for scanner.Scan() {
				fmt.Println(scanner.Text())
				result += scanner.Text()
			}
		}()

		for _, sql := range clientBody.Sql {
			fmt.Fprintln(stdin, sql)
		}

		err = cmd.Wait()
		if err != nil {
			fmt.Println(err)
			return
		}
	}
	c.JSON(http.StatusOK, gin.H{"msg": "交互成功", "token": clientBody.Token, "result": result})
}

func randomUUID() string {
	u4 := uuid.New()
	return u4.String()
}
