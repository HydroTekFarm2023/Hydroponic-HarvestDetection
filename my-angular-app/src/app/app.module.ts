import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http'; // Import the HttpClientModule

import { AppComponent } from './app.component';
import { ApiService } from './api.service';

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    // Add the HttpClientModule here
  ],
  providers: [ApiService], // Provide the ApiService here
  bootstrap: [AppComponent]
})
export class AppModule { }
