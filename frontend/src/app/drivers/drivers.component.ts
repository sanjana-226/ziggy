import { Component } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-drivers',
  templateUrl: './drivers.component.html',
  styleUrls: ['./drivers.component.css']
})
export class DriversComponent {
  drivers: any;
  constructor(private api:ApiService) { }

  getDrivers(){
    this.api.getDrivers().subscribe(res => {
      console.log(res);
      this.drivers=res;
    });
  }
}
