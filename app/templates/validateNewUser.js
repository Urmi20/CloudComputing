function validateNewUser()
{
	var username = document.forms["registration"]["username"];
	var first_name = document.forms["registration"]["first_name"];
	var last_name = document.forms["registration"]["last_name"];
	var email = document.forms["registration"]["email"];
	var password = document.forms["registration"]["password"];
	var password_conf = document.forms["registration"]["password_conf"];

	if (username.value == "")
	{
		window.alert("Please enter your name.");
		username.focus();
		return false;
	}

	if (first_name.value == "")
	{
		window.alert("Please enter your first name.");
		first_name.focus();
		return false;
	}

	if (last_name.value == "")
	{
		window.alert("Please enter your last name.");
		email.focus();
		return false;
	}

	if (email.value.indexOf("@", 0) < 0)
	{
		window.alert("Something is wrong");
		email.focus();
		return false;
	}

	if (password.value = "")
	{
		window.alert("Please enter a valid password.");
		password.focus();
		return false;
	}

	if (password_conf.value == "")
	{
		window.alert("Please enter the password confirmation.");
		password_conf.focus();
		return false;
	}

	return true;
}