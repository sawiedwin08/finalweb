import {Component} from '@angular/core';
import {ApiConection} from "../Shared/ApiConection";
import {MenubarModule} from 'primeng/menubar';
import {MenuItem} from "primeng/api";
import {TableModule} from 'primeng/table';
import {ButtonModule} from 'primeng/button';
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";
import { DialogModule } from 'primeng/dialog';
import {InputTextModule} from "primeng/inputtext";
@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    MenubarModule,
    TableModule,
    ButtonModule,
    DialogModule,
    ReactiveFormsModule,
    FormsModule,
    InputTextModule,
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  formParqueadero : FormGroup;
  formTarifa : FormGroup;
  items: MenuItem[] | undefined;
  parqueaderos: any[] = [];
  verFormParqueadero: boolean = false;
  selectedParqueadero: any = {};

  constructor(private api: ApiConection, private fb: FormBuilder) {
    this.api.token = localStorage.getItem('token')
    this.formParqueadero = this.fb.group({
      id:[''],
      nombre:['',Validators.required],
      nit :['',Validators.required],
      direccion:['',Validators.required],
      telefono:['',Validators.required]

    })
    this.formTarifa = this.fb.group({
      id:[''],
      parqueadero_id:['',Validators.required],
      tamano:['',Validators.required],
      precio :['',Validators.required],
    })
  }

  ngOnInit() {
    this.items = [
      {
        label: 'Home',
        icon: 'pi pi-home'
      },
    ]
    this.listaParqueaderos()
  }

  listar() {
    this.api.get('pareuadero')
      .subscribe(data => {
        console.log(data);
      })
  }

  listaParqueaderos() {
    console.log(this.api.token)
    this.api.get('parqueadero')
      .subscribe(
        data => {
          this.parqueaderos = data
        })
  }

  accionFormularioParqueadero(){
    if(this.formParqueadero.value['id']){
      this.updateParqueadero()
    }else {
      this.addParqueadero()
    }
  }

  addParqueadero() {

    this.api.add('parqueadero/', this.formParqueadero.value)
      .subscribe(
        data => {
          this.listaParqueaderos()
          this.verFormParqueadero  = false
          this.formParqueadero.reset()
        }
      )
  }

  updateParqueadero(){
    this.api.update('parqueadero', this.formParqueadero.value,this.selectedParqueadero.id)
      .subscribe(
        data => {
          this.listaParqueaderos()
          this.verFormParqueadero  = false
          this.formParqueadero.reset()
        }
      )
  }

  seleccionarParqueadero() {
    this.formParqueadero.patchValue(this.selectedParqueadero)
    this.verFormParqueadero = true
  }

  cancel(){
    this.formParqueadero.reset()
    this.verFormParqueadero = false
    this.selectedParqueadero = {}
  }
}
