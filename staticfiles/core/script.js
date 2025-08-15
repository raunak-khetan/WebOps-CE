document.addEventListener('DOMContentLoaded', function () {
	const formContainer = document.getElementById('team-members-container');
	const addMemberButton = document.getElementById('add-member-button');
	const deleteLastMemberButton = document.getElementById(
		'delete-last-member-button'
	);

	const registrationForm = document.getElementById('registration-form');
	console.log(registrationForm);

	registrationForm.addEventListener('submit', function (e) {
		const totalForms = document.getElementById('id_members-TOTAL_FORMS');
		const currentMemberCount = parseInt(totalForms.value, 10) + 1; // +1 to include the head

		let isValid = true; // Flag to check overall form validity
		let errorMessages = [];

		if (currentMemberCount < minParticipants) {
			isValid = false;
			errorMessages.push(`Minimum ${minParticipants} members required.`);
		}

		const phoneFields = document.querySelectorAll('input[name$="phone_no"]');
		console.log(phoneFields[0].value);

		function validatePhoneNumber(phoneNumber) {
			const phoneRegex = /^\d{10}$/;
			return phoneRegex.test(phoneNumber);
		}

		phoneFields.forEach(function (field) {
			const phoneValue = field.value.trim();
			if (!validatePhoneNumber(phoneValue)) {
				isValid = false;
				errorMessages.push(`Phone number "${phoneValue}" is invalid.`);
			}
		});

		// After all checks, only show toast if form is invalid
		if (!isValid) {
			e.preventDefault(); // Prevent form submission
			const errorContainer = document.createElement('div');

			errorMessages.forEach(function (message) {
				const messageDiv = document.createElement('div');
				messageDiv.textContent = message;
				errorContainer.appendChild(messageDiv);
			});

			// Display all error messages using Toastify
			Toastify({
				node: errorContainer,
				duration: 5000,
				gravity: 'top',
				position: 'right',
				backgroundColor: 'linear-gradient(to right, #ff5f6d, #ffc371)',
				escapeMarkup: false, // Allow line breaks
			}).showToast();
		}
	});

	function updateFormCount() {
		const totalForms = document.getElementById('id_members-TOTAL_FORMS');
		const numForms = formContainer.querySelectorAll('.team-member-form').length;
		const heading = document.querySelector('#teamMembersHead');

		totalForms.value = numForms;

		deleteLastMemberButton.style.display =
			numForms > 0 ? 'inline-block' : 'none';
		heading.style.display = numForms > 0 ? 'inline-block' : 'none';

		manageDeleteButtons();
		updateMemberNumbers();
		updateAddMemberButton(); // Ensure "Add Member" button is updated each time
	}

	function updateMemberNumbers() {
		const memberForms = formContainer.querySelectorAll('.team-member-form');
		memberForms.forEach((form, index) => {
			const header = form.querySelector('.index');
			if (header) {
				header.textContent = `${index + 1}`;
			}
		});
	}

	function manageDeleteButtons() {
		const memberForms = formContainer.querySelectorAll('.team-member-form');
		memberForms.forEach((form, index) => {
			const deleteButton = form.querySelector('#deletebtn');
			if (index === memberForms.length - 1) {
				deleteButton.style.display = 'none';
			} else {
				deleteButton.style.display = 'inline-block';
			}
		});
	}

	function updateAddMemberButton() {
		const totalForms = document.getElementById('id_members-TOTAL_FORMS');
		const currentMemberCount = parseInt(totalForms.value, 10) + 1; // +1 to include the head

		// Reset the button if the count is below maxParticipants
		if (currentMemberCount >= maxParticipants) {
			addMemberButton.disabled = true;
			addMemberButton.textContent = 'Limit reached';
		} else {
			addMemberButton.disabled = false;
			addMemberButton.innerHTML = `<i class="fa-solid fa-user-plus" style="color: #583400;"></i> Add Member`;
		}
	}

	deleteLastMemberButton.addEventListener('click', function () {
		const lastMemberForm = formContainer.querySelector(
			'.team-member-form:last-child'
		);
		if (lastMemberForm) {
			lastMemberForm.remove();
			updateFormCount(); // Update after deletion to check "Add Member" button status
		}
	});

	window.removeMember = function (button) {
		const memberForm = button.closest('.team-member-form');
		if (memberForm) {
			memberForm.remove();
			updateFormCount(); // Update after deletion
		}
	};

	addMemberButton?.addEventListener('click', function () {
		const totalForms = document.getElementById('id_members-TOTAL_FORMS');
		const currentMemberCount = parseInt(totalForms.value, 10) + 1; // +1 to include the head

		if (currentMemberCount >= maxParticipants) {
			Toastify({
				text: `Maximum ${maxParticipants} members allowed.`,
				duration: 3000,
				gravity: 'top',
				position: 'right',
				backgroundColor: 'linear-gradient(to right, #ff5f6d, #ffc371)',
			}).showToast();
			return;
		}

		const newMemberForm = document.createElement('div');
		newMemberForm.classList.add('team-member-form');
		newMemberForm.innerHTML =
			buildMemberFormHtml(currentMemberCount - 1) + dltbtn();

		formContainer.appendChild(newMemberForm);
		updateFormCount(); // Update after addition to check "Add Member" button status
	});

	window.copyField = function (source, target) {
		const sourceField = document.getElementById(source);
		const targetField = document.getElementById(target);
		if (sourceField && targetField) {
			targetField.value = sourceField.value;
		}
	};

	function dltbtn() {
		return `
            <button type="button" class="btn btn-danger" id="deletebtn" onclick="removeMember(this)">
                <i class="fa-solid fa-user-minus" style="color: #583400;"></i> Delete Member
            </button>
        `;
	}

	function buildMemberFormHtml(index) {
		return `
            <div class="form-header">
                <h3>Member's Data</h3>
                <span><span class="preindex">Member no.</span> <span class="index">${
									index + 1
								}</span></span>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Member's Name <span class="astrick">*</span></label>
                    <div class="input-group">
                        <input type="text" name="members-${index}-name" id="id_members-${index}-name" class="form-control" required/>
                    </div>
                </div>
                <div class="form-group">
                    <label>Gender <span class="astrick">*</span></label>
                    <select name="members-${index}-gender" id="id_members-${index}-gender" class="form-control" required>
                        <option value="">Select</option>
                        <option value="M">Male</option>
                        <option value="F">Female</option>
                        <option value="O">Other</option>
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Member's Contact Number <span class="astrick">*</span></label>
                    <div class="input-group">
                        <input type="text" name="members-${index}-phone_no" id="id_members-${index}-phone_no" class="form-control" required />
                    </div>
                </div>
                <div class="form-group">
                    <label>E-Mail <span class="astrick">*</span></label>
                    <div class="input-group">
                        <input type="email" name="members-${index}-email" id="id_members-${index}-email" class="form-control" required />
                        <button type="button" class="btn-input-append" onclick="copyField('id_email', 'id_members-${index}-email')">Same as leader</button>
                    </div>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Program Enrolled <span class="astrick">*</span></label>
                    <div class="input-group">
                        <input type="text" name="members-${index}-program_enrolled" id="id_members-${index}-program_enrolled" class="form-control" required />
                        <button type="button" class="btn-input-append" onclick="copyField('id_program_enrolled', 'id_members-${index}-program_enrolled')">Same as leader</button>
                    </div>
                </div>
                <div class="form-group">
                    <label>Institute Name <span class="astrick">*</span></label>
                    <div class="input-group">
                        <input type="text" name="members-${index}-institute_name" id="id_members-${index}-institute_name" class="form-control" required/>
                        <button type="button" class="btn-input-append" onclick="copyField('id_institute_name', 'id_members-${index}-institute_name')">Same as leader</button>
                    </div>
                </div>
                <div class="form-group">
                    <label>Year of Passing <span class="astrick">*</span></label>
                    <div class="input-group">
                        <input type="text" name="members-${index}-year_of_passing" id="id_members-${index}-year_of_passing" class="form-control" required/>
                        <button type="button" class="btn-input-append" onclick="copyField('id_year_of_passing', 'id_members-${index}-year_of_passing')">Same as leader</button>
                    </div>
                </div>
            </div>
        `;
	}

	updateFormCount(); // Initialize form count
});
