import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

import { AppComponent } from './app.component'

import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { AngularMaterialModule } from './angular-material.module';



@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [

    BrowserModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    AngularMaterialModule
    
  ],
  
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
