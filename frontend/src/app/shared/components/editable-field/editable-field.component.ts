import { Component, model, output, signal } from '@angular/core';
import { InplaceModule } from 'primeng/inplace';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'sha-editable-field',
  templateUrl: 'editable-field.component.html',
  imports: [InplaceModule, InputTextModule, ButtonModule, FormsModule],
})
export class EditableFieldComponent {
  readonly data = model.required<{ key: string; value: string | number | Date }>();
  protected readonly editMode = signal(false);
  readonly updateField = output<{}>();

  onClickInput() {
    this.editMode.set(true);
    console.log('dasdsadas');
  }
  onClose() {
    this.editMode.set(false);
    console.log('close');
  }
  onSave(inputValue: ReturnType<typeof this.data>) {
    if (inputValue !== this.data()) {
      this.updateField.emit({ [inputValue.key]: inputValue.value });
      this.data.set(inputValue);
    }
    this.editMode.set(false);
  }
}
