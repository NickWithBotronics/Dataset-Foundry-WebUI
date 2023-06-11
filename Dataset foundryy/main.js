// Helper function to post form data and get result
async function postForm(url, formData, resultId) {
    try {
        let response = await $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            processData: false, 
            contentType: false,
        });

        $(`#${resultId}`).text(response);
    } catch (error) {
        console.error("Error: ", error);
    }
}

// Foundry form
$("#foundryForm").submit(async function(e) {
    e.preventDefault();
    let formData = new FormData(this);
    await postForm('/run_foundry', formData, 'foundryResult');
});

// Tokens form
$("#tokensForm").submit(async function(e) {
    e.preventDefault();
    let formData = new FormData(this);
    await postForm('/count_tokens', formData, 'tokensResult');
});

// Cost form
$("#costForm").submit(async function(e) {
    e.preventDefault();
    let formData = new FormData(this);
    await postForm('/calculate_cost', formData, 'costResult');
});

// Format form
$("#formatForm").submit(async function(e) {
    e.preventDefault();
    let formData = new FormData(this);
    await postForm('/format_dataset', formData, 'formatResult');
});
