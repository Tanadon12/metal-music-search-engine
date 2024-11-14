// function performSearch() {
//     const query = document.getElementById('search-input').value.trim();
//     const resultsPerPage = document.getElementById('results-per-page').value || 8;
//     const page = 1; // Start with page 1

//     if (!query) {
//         alert("Please enter a search term.");
//         return;
//     }

//     fetch(`/search?q=${encodeURIComponent(query)}&results_per_page=${resultsPerPage}&page=${page}`)
//         .then(response => response.json())
//         .then(data => {
//             if (data.error) {
//                 document.getElementById('results').innerHTML = `<p>Error: ${data.error}</p>`;
//                 return;
//             }

//             const hits = data.hits;
//             const resultsDiv = document.getElementById('results');
//             resultsDiv.innerHTML = ''; // Clear previous results

//             if (hits.length > 0) {
//                 hits.forEach(hit => {
//                     const song = hit.content;
//                     const songHTML = `
//                         <div class="song-result">
//                             <h3>${song['Song Name']}</h3>
//                             <p><strong>Artist:</strong> ${song['Artist/Band']}</p>
//                             <p><strong>Album:</strong> ${song['Album Name']}</p>
//                             <p><strong>Duration:</strong> ${song['Duration']}</p>
//                             <p><strong>Release Date:</strong> ${song['Release Date']}</p>
//                             <img src="${song['Image']}" alt="Album Art" width="100">
//                             <p><strong>Lyrics:</strong> ${song['Lyrics'].slice(0, 200)}...</p>
//                         </div>
//                     `;
//                     resultsDiv.innerHTML += songHTML;
//                 });
//             } else {
//                 resultsDiv.innerHTML = '<p>No results found.</p>';
//             }

//             // Update pagination info
//             document.getElementById('page-info').innerText = `Page ${data.page_no} of ${data.page_total}`;
//         })
//         .catch(error => {
//             document.getElementById('results').innerHTML = `<p>Error: ${error.message}</p>`;
//         });
// }

function updateResultsPerPage() {
    const resultsPerPage = document.getElementById('results-per-page').value;
    const keyword = new URLSearchParams(window.location.search).get('keyword');
    if (keyword) {
        window.location.href = `/search?keyword=${keyword}&results_per_page=${resultsPerPage}`;
    }
}

