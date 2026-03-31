# SkyNote

Cloud Notes API with authentication.

---

## Stack
Flask • SQLite • Docker • AWS EC2 • Terraform

---

## Features
- User registration + login  
- Token-based authentication  
- User-specific data (notes per user)  
- Full CRUD API  
- Persistent storage (Docker volume)  
- Deployed on AWS  

---

## Example

Register:
curl -X POST http://YOUR_IP/register -H "Content-Type: application/json" -d '{"username":"test","password":"123456"}'

Login:
curl -X POST http://YOUR_IP/login -H "Content-Type: application/json" -d '{"username":"test","password":"123456"}'

Use token:
curl http://YOUR_IP/notes -H "Authorization: Bearer YOUR_TOKEN"

---

## Built to practice for college
Backend • Auth • Database • Docker • Cloud deployment
