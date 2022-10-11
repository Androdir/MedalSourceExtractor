$("#submit").on("click", e => {
	$("#submit").attr("disabled", true);
	$("#video-container").html(`<div class="spinner-border text-primary">`);
	$("#extracted-url").val("");
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