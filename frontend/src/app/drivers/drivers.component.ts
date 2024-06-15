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

  ngOnInit() {
    this.getDrivers();
    console.log('init');
    console.log(this.drivers);
    
  }

  onRefresh() {
    this.getDrivers();
    console.log('refresh');
    console.log(this.drivers);
  }

  ngAfterViewInit() {
    this.getDrivers();
    console.log('init');
    console.log(this.drivers);
  }

  getDrivers() {
    this.api.getDrivers().subscribe(data => {
      this.drivers = data;
      console.log(this.drivers);
    }, error => {
      console.error('Error fetching drivers:', error);
    });
  }
 
}
