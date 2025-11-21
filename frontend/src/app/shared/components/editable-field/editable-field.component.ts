import { Component, model, OnInit, output, signal } from '@angular/core';
import { InplaceModule } from 'primeng/inplace';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'sha-editable-field',
  templateUrl: 'editable-field.component.html',
  imports: [InplaceModule, InputTextModule, ButtonModule, FormsModule],
})
export class EditableFieldComponent implements OnInit {
  readonly data = model.required<{ label: string; value: any; type: string; key: string }>();
  protected readonly editMode = signal(false);
  readonly updateField = output<{}>();
  inputValue = null;

  ngOnInit() {
    this.inputValue = this.data().value;
  }
  onBlur(event: FocusEvent) {
    event.stopPropagation();
    if (!document.hasFocus()) {
      return;
    }
    this.onClose();
  }

  onClickInput() {
    this.editMode.set(true);
  }

  onClose() {
    this.inputValue = this.data().value;
    this.editMode.set(false);
  }

  onSave() {
    if (this.inputValue !== this.data().value) {
      this.updateField.emit({ [this.data().key]: this.inputValue });
      this.data.update((data) => ({ ...data, value: this.inputValue }));
    }
    this.editMode.set(false);
  }
}
