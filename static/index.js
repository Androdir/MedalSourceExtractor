$("#submit").on("click", e => {
	$("#submit").attr("disabled", true);
	$("#video-container").html(`<div class="spinner-border text-primary">`);
	$("#extracted-url").val("");
	if (!$("#url-input").val().toLowerCase().includes("medal")) {
		alert("That is not a valid link. Do not enter any other links except for the one you got from Medal.tv");
		$("#submit").attr("disabled", false);
		$("#video-container").html("");
		return;
	}
	fetch("/api/extract", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"Accept": "application/json",
			"url": $("#url-input").val()
		},
	}).then(response => {
		response.json().then(data => {
			$("#submit").attr("disabled", false);
			$("video").remove();
			$("#video-container").html(`<video src="${data}" type="video/mp4" controls></video>`);
			$("#extracted-url").val(data);
		})
	});
});

$("#copy").on("click", e => {
	navigator.clipboard.writeText($("#extracted-url").val());
})