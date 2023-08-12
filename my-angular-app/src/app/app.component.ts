import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';
import { AxiosResponse } from 'axios';
import { saveAs } from 'file-saver';

import { ApiService } from './api.service';
import axios from 'axios-observable';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  apiData: string='data will arrive';
  test: any;
  selectedImage: File | null = null; // Holds the selected image file

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {
    // Call the API when the component initializes
    // this.fetchDataFromApi();
  }

  
  
  fetchDataFromApi(): void {
    if (!this.selectedImage) {
      console.error('No image selected');
      return;
    }
    
function mapValuesToClasses(str: string, classes: string[]): { [key: string]: { count: number; }; } {
  const values = str.split(',').map(Number);
  const result: { [key: string]: { count: number; }; } = {};

  for (let i = 0; i < values.length; i++) {
    const value = values[i];
    const className = classes[value - 1];
    if (className) {
      if (result[className]) {
        result[className].count++;
      } else {
        result[className] = { count: 1 };
      }
    }
  }

  return result;
}
  
 function countOccurrences(obj: { [key: string]: {  count: number; }; }): { [key: string]: { count: number; }; } {
  const result: { [key: string]: { count: number; }; } = {};

  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const { count } = obj[key];
      result[key] = { count: count };
    }
  }

  return result;
}




    const formData = new FormData();
    formData.append('file', this.selectedImage);

    // Replace 'YOUR_API_ENDPOINT' with the actual API endpoint URL
    const apiEndpoint = 'http://127.0.0.1:80/';

    // Make the API call using Axios-observable
    axios.post<any>(apiEndpoint, formData)
      .subscribe(
        (response: AxiosResponse<any>) => {
          // console.log('API Response:', response.data);
          // this.apiData = response.data; // Save the API response data
          const inputString = (response.data).toString();

          const classes = ['red', 'white', 'ripe', 'green'];

          const mappedValues = mapValuesToClasses((inputString), classes);
          const occurrences = countOccurrences(mappedValues);

          console.log("Mapped Values:", mappedValues);
          console.log("Occurrences:", occurrences);

          const beautifiedOccurrences = JSON.stringify(occurrences, null, 2);
          const beautifiedMappedValues = JSON.stringify(mappedValues, null, 2);

          // Remove double quotes and brackets
          const formattedOccurrences = beautifiedOccurrences.replace(/"|{|}/g, '');
          const formattedMappedValues = beautifiedMappedValues.replace(/"|{|}/g, '');

          // Concatenate both strings
          const resultString = `Occurrences of strawbebbery:\n${formattedOccurrences}\n\n  \n${formattedMappedValues}`;

          // Print the final formatted string
          this.apiData = resultString;
        },
        (error) => {
          console.error('API Error:', error);
        }
    );
        
  }

  onFileSelected(event: any): void {
    const file: File = event.target.files[0];
    this.selectedImage = file;
  }
}
