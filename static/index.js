$("button").on("click", (e) => {
	fetch("/api/extract", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"Accept": "application/json",
			"url": $("input").val()
		},
	}).then(response => {
		response.json().then(data => {
			$("#pp").html(data);
		})
	});
});