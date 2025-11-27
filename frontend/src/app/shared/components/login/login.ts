import { Component, inject } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { AuthService } from '../../../core/services/auth.service';
import { ButtonModule } from 'primeng/button';
import { Router } from '@angular/router';
import { IftaLabelModule } from 'primeng/iftalabel';
import { MessageModule } from 'primeng/message';

@Component({
  imports: [
    ReactiveFormsModule,
    PasswordModule,
    InputTextModule,
    ButtonModule,
    IftaLabelModule,
    MessageModule,
  ],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  loginForm = new FormGroup({
    username: new FormControl('', [Validators.required]),
    password: new FormControl('', Validators.required),
  });

  private authService = inject(AuthService);
  private router = inject(Router);

  onSubmit() {
    console.log('login');
    
    const val = this.loginForm.value;
    if (this.loginForm.invalid) return;
    if (val.username && val.password) {
      const error = this.authService.login(val.username, val.password);
    }
    this.router.navigate(['/']);
  }
}
