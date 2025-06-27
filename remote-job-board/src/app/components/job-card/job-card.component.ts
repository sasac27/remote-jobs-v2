import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-job-card',
  imports: [],
  templateUrl: './job-card.component.html',
  styleUrl: './job-card.component.scss'
})
export class JobCardComponent {
  @Input() job: any;

}
