import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [],
  templateUrl: './landing.component.html',
  styleUrl: './landing.component.css'
})
export class LandingComponent {
  flag:any;
  constructor(public http:HttpClient,public router:Router)
  {

  }
  signin()
  {
    this.flag=0;
    this.http.post("http://127.0.0.1:8000/login",{},{observe:"response"}).subscribe(body=>{
      this.flag=1;
      console.log("Hello");
    });
    
    this.router.navigateByUrl("home");
  }
}
