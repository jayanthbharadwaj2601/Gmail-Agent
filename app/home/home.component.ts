import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {

  constructor(public http:HttpClient,public router:Router)
  {

  }
  draft(recipients:string,subject:string)
  {
    this.http.post("http://127.0.0.1:8000/",{fromid:"kidambi.jayanth@gmail.com",toid:recipients,body:subject},{observe:"response"}).subscribe(body=>{
      console.log("success");
    });
    alert("Drafts created Successfully,check your drafts section");
  }
  send(recipients:string,subject:string)
  {
    this.http.post("http://127.0.0.1:8000/send",{fromid:"kidambi.jayanth@gmail.com",toid:recipients,body:subject},{observe:"response"}).subscribe(body=>{
      console.log("success");
    });
    alert("Message sent successfully");
  }
}
