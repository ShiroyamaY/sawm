function validateLoginForm(event) {
	const login = document.getElementById('login').value;
	const password = document.getElementById('password').value;
	const re = /^[A-Za-z0-9_]{3,32}$/;
	if (!re.test(login) || !re.test(password)) {
		alert('Invalid input: only letters, digits, underscore (3-32).');
		event.preventDefault();
		return false;
	}
	return true;
}



