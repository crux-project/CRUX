import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { map, Observable, startWith } from 'rxjs';
// PATH TO technique JSON FILE
import data from '../assets/json/data.json';
import unit from '../assets/json/unit.json';
console.log

declare function autocomplete(inp:any,arr:any): any;



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {

  myForm = new FormGroup({
  //  technique: new FormControl('', [Validators.required]),
  technique: new FormControl(''),
   parameter1: new FormControl('', [Validators.required]),
   parameter2: new FormControl(''),
   parameter3: new FormControl(''),
   value1: new FormControl(''),
   value2: new FormControl(''),
   value3: new FormControl(''),
   unit1: new FormControl('', [Validators.required]),
   unit2: new FormControl(''),
   unit3: new FormControl(''),
   file: new FormControl('', [Validators.required]),
   fileSource: new FormControl('', [Validators.required])
 });
  
  //  = ['Sintering',
  // 'Pulsed laser deposition',
  // 'Thermal Curing',
  // 'Etching',
  // 'Magnetron Sputtering',
  // 'Thermal Atomic Layer Deposition',
  // 'Czochralski method',
  // 'Laser Powder Bed Fusion',
  // 'Spark Plasma Sintering',
  // 'Spin Casting',
  // 'Arc Melting',
  // 'Wire Drawing',
  // 'Anodization',
  // 'Forging',
  // 'Gas atomization ',
  // 'Laser Powder bed Fusion (LPBF)',
  // 'Electron Beam Melting (EBM)',
  // 'Fused deposition modeling (FDM)',
  // 'Annealing',
  // 'Friction Stir Welding (FSW)',
  // 'Hot Isostatic Pressing (HIP)',
  // 'Quenching',
  // 'Precipitation hardening/aging',
  // 'Laser Hot-Wire',
  // 'Wire Arc Additive Manufacturing',
  // 'Welding',
  // 'Direct metal laser sintering (DMLS)',
  // 'Selective laser melting (SLM)',
  // 'Electron Beam Melting',
  // 'Sciaky',
  // 'Laser Engineered Net Shaping (LENS)',
  // 'Laser Metal Deposition (LMD)',
  // 'Direct metal deposition (DMD)',
  // 'Ball Milling',
  // 'Induction Melting',
  // 'Electroplating',
  // 'Austenitization',
  // 'Ultrasonic Additive Manufacturing',
  // 'Computer-Aided Manufacturing of Laminated Engineering Materials (CAM-LEM) ',
  // 'Joule Printing',
  // 'Atomic Diffusion AM (ADAM)',
  // 'Fused Deposition Modeling (FDM)',
  // 'Extrusion',
  // 'UV Curing',
  // 'Spin coating',
  // 'Flame fusion',
  // 'Solvothermal processing',
  // 'Tape transfer exfolitation',
  // 'Casting (solvent)'];

  parameter:any[] = ['temperature','atmosphere','time','pressure','laser fluence','laser frequency',
  'ramp rates','duration','ph','dwell time','pulse frequency','growth time','precursors',
  'carrier gas','flow rate','pull rate','rotation rate','composition','laser power','scan speed',
  'voltage','foil','acceleration','current','reduction','tension','current density',
  'solution','gas/metal ratio','power','layer thickness','hatch spacing',
  'preheat temperature',
  'head temperature',
  'feed rate',
  'thickness',
  'infill',
  'rotation speed',
  'travel speed',
  'heat input',
  'cooling rate',
  'quench media',
  'quench',
  'hot wire power',
  'wire feed speed',
  'velocity',
  'overlap',
  'arc',
  'shielding gas',
  'building direction',
  'accelerating voltage',
  'beam current',
  'power density',
  'vacuum level',
  'powder feed rate',
  'gas flow rate',
  'traverse rate',
  'ball size',
  'ball material',
  'powder diameter',
  'wattage',
  'frequency',
  'ion concentration',
  'ultrasonic amplitude',
  'applied normal force',
  'texture of horn',
  'sintering temperature',
  'head travel speed',
  'deposition strategy',
  'sintering time',
  'extrusion rate',
  'die size',
  'wavelength',
  'fluence',
  'rotation rate(s)',
  'particle size',
  'solvent/flux',
  'tape type',
  'solvent'] ;

  products: any = [];
  technique:any = [];
  units: any = [];
  filteredOptions: Observable<any> = new Observable<any>();
  isUploadDisabled:boolean = true;
  isSubmitDisabled:boolean = true;
  constructor(private http: HttpClient) { }

  stringifiedData: any;  
  parsedJson: any;  

  
 ngOnInit() {
  // this.filteredOptions = this.myForm.get('technique')?.valueChanges
  //   .pipe(
  //     startWith(''),
  //     map(value => this._filter(value))
  //   );
  // autocomplete('',this.technique);
  this.http.get("assets/json/data.json").subscribe(data =>{
    // console.log(data);
     for(let i=0;i<=Object.keys(data).length;i++){
       this.products.push(Object.values(data)[i]);
       this.technique.push(Object.values(data)[i].technique);
    }
    console.log(this.products)
  })

  this.http.get("assets/json/unit.json").subscribe(data =>{
    console.log(data);
    this.units = data;
  })

//   this.myForm.get('technique')?.valueChanges.subscribe((data:any)=>
//   {
//     if(data){
//     this.onchangetechnique();
//   }
// });
this.myForm.get('parameter1')?.valueChanges.subscribe((data:any)=>
{
  if(data){
  this.onchangeparameter(1);
}
});
this.myForm.get('parameter2')?.valueChanges.subscribe((data:any)=>
{
  if(data){
  this.onchangeparameter(2);
}
});
this.myForm.get('parameter3')?.valueChanges.subscribe((data:any)=>
{
  if(data){
  this.onchangeparameter(3);
}
});
}
 get f(){
   return this.myForm.controls;
 }
    
 onFileChange(event:any) {
 
   if (event.target.files.length > 0) {
     const file = event.target.files[0];
     this.myForm.patchValue({
       fileSource: file
     });
   }
 }
    
 submit(){
   
  const formData = new FormData();
  if(this.myForm.value!=null){
    if(!this.technique.includes(this.myForm.get('technique')?.value)){
      // this.isSubmitDisabled=true;
      // alert('Please Upload Data.!');
      // this.isUploadDisabled=false;
      this.UploadData();
    }
    // else{
    //   // this.isUploadDisabled=true;
    //   // this.isSubmitDisabled=false;
    //   this.UploadData();
    // } 
  }  

 }

UploadData(){
  const formData = new FormData();
  formData.append('file', this.myForm.get('fileSource')?.value);
   this.http.post('http://localhost:8001/upload.php', formData)
   
     .subscribe(res => {
       console.log(res);
       alert('Uploaded Successfully.');
     })
}
 private _filter(value: string): string[] {
  const filterValue = value.toLowerCase();

  return this.technique.filter((option: string) => option.toLowerCase().includes(filterValue));
}
onchangeparameter(event:any){
if (event == 1) {
  autocomplete(document.getElementById("parameter1"), this.parameter); 
} else if (event == 2){
  autocomplete(document.getElementById("parameter2"), this.parameter);
} else {
  autocomplete(document.getElementById("parameter3"), this.parameter);
}
}

onchangetechnique(){
  // let technique:any;
//   for(let i=0;i<=this.products.length;i++){
//     // console.log("TECH : "+this.products[i].technique);
//     // if (this.products.hasOwnProperty(technique)) {
//     //     console.log(technique + " = " + this.products[technique]);
//     // }
// } 
  autocomplete(document.getElementById("technique"), this.technique);
  console.log(this.myForm.get('technique')?.value)
  
}
changeUnit1(e:any) {
  console.log(e.value)
  this.unit1?.setValue(e.target.value, {
    onlySelf: true
  })
}
changeUnit2(e:any) {
  console.log(e.value)
  this.unit2?.setValue(e.target.value, {
    onlySelf: true
  })
}
changeUnit3(e:any) {
  console.log(e.value)
  this.unit3?.setValue(e.target.value, {
    onlySelf: true
  })
}
get unit1() {
  return this.myForm.get('unit1');
}
get unit2() {
  return this.myForm.get('unit2');
}
get unit3() {
  return this.myForm.get('unit3');
}
}