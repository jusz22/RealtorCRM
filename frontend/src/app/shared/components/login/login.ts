import { Component, inject } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { AuthService } from '../../../core/services/auth.service';
import { ButtonModule } from 'primeng/button';
import { Router } from '@angular/router';
import { IftaLabelModule } from 'primeng/iftalabel';
import { MessageModule } from 'primeng/message';
import { HttpErrorResponse } from '@angular/common/http';
import { CardModule } from 'primeng/card';

@Component({
  imports: [
    ReactiveFormsModule,
    PasswordModule,
    InputTextModule,
    ButtonModule,
    IftaLabelModule,
    MessageModule,
    CardModule,
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
    const val = this.loginForm.value;
    if (this.loginForm.invalid) return;
    if (val.username && val.password) {
      this.authService.login(val.username, val.password).subscribe({
        next: (res) => {
          this.authService.saveToken(res);
          this.router.navigate(['/']);
        },
        error: (err: HttpErrorResponse) => {
          if (err.status === 401) {
            return { error: 'Wrong login or password' };
          }
          if (err.status && err.status !== 401) return { error: 'Error' };
          return;
        },
      });
    }
  }
}
