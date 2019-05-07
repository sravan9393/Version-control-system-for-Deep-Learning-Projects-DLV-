import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { StorageServiceModule} from 'ngx-webstorage-service';

import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import {AppRoutingModule} from './app-routing/app-routing.module';
import {
  MatButtonModule,
  MatCardModule, MatDatepickerModule,
  MatDialogModule, MatFormFieldModule, MatGridList, MatGridListModule,
  MatIconModule, MatInputModule, MatLabel,
  MatListModule, MatNativeDateModule,
  MatProgressBarModule, MatSidenavModule, MatTabsModule,
  MatToolbarModule, MatTreeModule
} from '@angular/material';
import { RegisterComponent } from './register/register.component';
import { LoginComponent } from './login/login.component';
import { UserReposComponent } from './user-repos/user-repos.component';
import { UploadDialogComponent } from './upload-dialog/upload-dialog.component';
import {UploadService} from './upload.service';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {HttpClientModule} from '@angular/common/http';
import {LocalStorageService} from './local-storage.service';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { ControlMessagesComponent } from './control-messages/control-messages.component';
import {ValidationService} from './validation.service';
import { RepositoryViewComponent } from './repository-view/repository-view.component';
import { RepoCodeComponent } from './repo-code/repo-code.component';
import { RepoChangesComponent } from './repo-changes/repo-changes.component';
import { RepoHistoryComponent } from './repo-history/repo-history.component';
import { FileDiffComponent } from './file-diff/file-diff.component';
import { SafeHtmlPipe } from './safe-html.pipe';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    RegisterComponent,
    LoginComponent,
    UserReposComponent,
    UploadDialogComponent,
    ControlMessagesComponent,
    RepositoryViewComponent,
    RepoCodeComponent,
    RepoChangesComponent,
    RepoHistoryComponent,
    FileDiffComponent,
    SafeHtmlPipe
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatToolbarModule,
    MatIconModule,
    MatButtonModule,
    MatCardModule,
    MatDialogModule,
    MatProgressBarModule,
    MatListModule,
    BrowserAnimationsModule,
    HttpClientModule,
    StorageServiceModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatTabsModule,
    MatListModule,
    MatTreeModule,
    MatSidenavModule,
    MatGridListModule
  ],
  entryComponents: [UploadDialogComponent],
  providers: [UploadService, HttpClientModule, LocalStorageService, ValidationService],
  bootstrap: [AppComponent]
})
export class AppModule { }
