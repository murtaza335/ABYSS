// Sample movie data
const movies = [
    {
        id: 1,
        title: "Inception",
        year: 2010,
        director: "Christopher Nolan",
        producers: ["Emma Thomas", "Christopher Nolan"],
        genre: ["sci-fi", "action", "thriller"],
        rating: 8.8,
        ageRating: "PG-13",
        poster: "/api/placeholder/250/350",
        actors: ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"],
        description: "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
    },
    {
        id: 2,
        title: "The Shawshank Redemption",
        year: 1994,
        director: "Frank Darabont",
        producers: ["Niki Marvin"],
        genre: ["drama"],
        rating: 9.3,
        ageRating: "R",
        poster: "/api/placeholder/250/350",
        actors: ["Tim Robbins", "Morgan Freeman"],
        description: "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
    },
    {
        id: 3,
        title: "The Dark Knight",
        year: 2008,
        director: "Christopher Nolan",
        producers: ["Emma Thomas", "Christopher Nolan", "Charles Roven"],
        genre: ["action", "thriller", "drama"],
        rating: 9.0,
        ageRating: "PG-13",
        poster: "/api/placeholder/250/350",
        actors: ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
        description: "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
    },
    {
        id: 4,
        title: "Pulp Fiction",
        year: 1994,
        director: "Quentin Tarantino",
        producers: ["Lawrence Bender"],
        genre: ["crime", "drama"],
        rating: 8.9,
        ageRating: "R",
        poster: "/api/placeholder/250/350",
        actors: ["John Travolta", "Uma Thurman", "Samuel L. Jackson"],
        description: "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."
    },
    {
        id: 5,
        title: "The Godfather",
        year: 1972,
        director: "Francis Ford Coppola",
        producers: ["Albert S. Ruddy"],
        genre: ["crime", "drama"],
        rating: 9.2,
        ageRating: "R",
        poster: "/api/placeholder/250/350",
        actors: ["Marlon Brando", "Al Pacino", "James Caan"],
        description: "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."
    },
    {
        id: 6,
        title: "The Matrix",
        year: 1999,
        director: "Lana and Lilly Wachowski",
        producers: ["Joel Silver"],
        genre: ["sci-fi", "action"],
        rating: 8.7,
        ageRating: "R",
        poster: "/api/placeholder/250/350",
        actors: ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
        description: "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."
    },
    {
        id: 7,
        title: "Parasite",
        year: 2019,
        director: "Bong Joon-ho",
        producers: ["Kwak Sin-ae", "Bong Joon-ho"],
        genre: ["drama", "thriller"],
        rating: 8.6,
        ageRating: "R",
        poster: "/api/placeholder/250/350",
        actors: ["Song Kang-ho", "Lee Sun-kyun", "Cho Yeo-jeong"],
        description: "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan."
    },
    {
        id: 8,
        title: "Get Out",
        year: 2017,
        director: "Jordan Peele",
        producers: ["Sean McKittrick", "Jason Blum", "Edward H. Hamm Jr.", "Jordan Peele"],
        genre: ["horror", "thriller"],
        rating: 7.7,
        ageRating: "R",
        poster: "/api/placeholder/250/350",
        actors: ["Daniel Kaluuya", "Allison Williams", "Bradley Whitford"],
        description: "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception of him eventually reaches a boiling point."
    },
    {
        id: 9,
        title: "Avengers: Endgame",
        year: 2019,
        director: "Anthony and Joe Russo",
        producers: ["Kevin Feige"],
        genre: ["action", "adventure", "sci-fi"],
        rating: 8.4,
        ageRating: "PG-13",
        poster: "/api/placeholder/250/350",
        actors: ["Robert Downey Jr.", "Chris Evans", "Mark Ruffalo"],
        description: "After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos' actions and restore balance to the universe."
    },
    {
        id: 10,
        title: "Toy Story",
        year: 1995,
        director: "John Lasseter",
        producers: ["Ralph Guggenheim", "Bonnie Arnold"],
        genre: ["animation", "adventure", "comedy"],
        rating: 8.3,
        ageRating: "G",
        poster: "/api/placeholder/250/350",
        actors: ["Tom Hanks", "Tim Allen"],
        description: "A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room."
    },
    {
        id: 11,
        title: "Barbie",
        year: 2023,
        director: "Greta Gerwig",
        producers: ["David Heyman", "Margot Robbie", "Tom Ackerley", "Robbie Brenner"],
        genre: ["comedy", "adventure"],
        rating: 7.0,
        ageRating: "PG-13",
        poster: "/api/placeholder/250/350",
        actors: ["Margot Robbie", "Ryan Gosling"],
        description: "Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land. However, when they get a chance to go to the real world, they soon discover the joys and perils of living among humans."
    },
    {
        id: 12,
        title: "Oppenheimer",
        year: 2023,
        director: "Christopher Nolan",
        producers: ["Emma Thomas", "Charles Roven", "Christopher Nolan"],
        genre: ["biography", "drama", "history"],
        rating: 8.5,
        ageRating: "R",
        poster: "/api/placeholder/250/350",
        actors: ["Cillian Murphy", "Emily Blunt", "Robert Downey Jr."],
        description: "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb."
    }
];

// DOM Elements
const mainSearch = document.getElementById('main-search');
const searchButton = document.getElementById('search-button');
const toggleFiltersButton = document.getElementById('toggle-filters');
const filtersSection = document.getElementById('filters-section');
const filterArrow = document.getElementById('filter-arrow');
const applyFiltersButton = document.getElementById('apply-filters');
const resetFiltersButton = document.getElementById('reset-filters');
const movieGrid = document.getElementById('movie-grid');
const modal = document.getElementById('movie-modal');
const closeModalButton = document.querySelector('.close-modal');

// Function to render movie cards
function renderMovies(moviesList) {
    movieGrid.innerHTML = '';
    
    if (moviesList.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'no-results';
        noResults.innerHTML = '<h3>No movies found matching your search</h3>';
        movieGrid.appendChild(noResults);
        return;
    }
    
    moviesList.forEach(movie => {
        const movieCard = document.createElement('div');
        movieCard.className = 'movie-card';
        movieCard.dataset.id = movie.id;
        
        movieCard.innerHTML = `
            <div class="movie-poster">
                <img src="${movie.poster}" alt="${movie.title} poster">
                <div class="movie-rating">${movie.rating}/10</div>
                <div class="movie-age-rating">${movie.ageRating}</div>
            </div>
            <div class="movie-info">
                <h3 class="movie-title">${movie.title}</h3>
                <div class="movie-genre">
                    ${movie.genre.map(g => `<span class="tag">${g}</span>`).join('')}
                </div>
                <div class="movie-year">${movie.year} • ${movie.director}</div>
            </div>
        `;
        
        movieCard.addEventListener('click', () => openMovieModal(movie.id));
        
        movieGrid.appendChild(movieCard);
    });
}

// Function to filter movies
function filterMovies() {
    const searchText = mainSearch.value.toLowerCase();
    const genreFilter = document.getElementById('genre').value;
    const yearFilter = document.getElementById('year').value;
    const ratingFilter = parseFloat(document.getElementById('rating').value) || 0;
    const ageRatingFilter = document.getElementById('age-rating').value;
    
    let filteredMovies = movies.filter(movie => {
        // Search filter
        if (searchText) {
            const producersString = movie.producers ? movie.producers.join(' ') : '';
            const searchableText = `${movie.title} ${movie.director} ${producersString} ${movie.actors.join(' ')} ${movie.genre.join(' ')}`.toLowerCase();
            if (!searchableText.includes(searchText)) {
                return false;
            }
        }
        
        // Genre filter
        if (genreFilter && !movie.genre.includes(genreFilter)) {
            return false;
        }
        
        // Year filter
        if (yearFilter) {
            if (yearFilter === 'older' && movie.year > 2018) {
                return false;
            } else if (yearFilter !== 'older' && movie.year != parseInt(yearFilter)) {
                return false;
            }
        }
        
        // Rating filter
        if (movie.rating < ratingFilter) {
            return false;
        }
        
        // Age Rating filter
        if (ageRatingFilter && movie.ageRating !== ageRatingFilter) {
            return false;
        }
        
        return true;
    });
    
    renderMovies(filteredMovies);
}

// Function to open movie modal
function openMovieModal(movieId) {
    const movie = movies.find(m => m.id === movieId);
    if (!movie) return;
    
    const modalTitle = document.getElementById('modal-title');
    const modalImg = document.getElementById('modal-img');
    const modalMeta = document.getElementById('modal-meta');
    const modalAgeRating = document.getElementById('modal-age-rating');
    const modalGenres = document.getElementById('modal-genres');
    const modalDescription = document.getElementById('modal-description');
    const modalCast = document.getElementById('modal-cast');
    const modalProduction = document.getElementById('modal-production');
    
    modalTitle.textContent = movie.title;
    modalImg.src = movie.poster;
    modalImg.alt = `${movie.title} poster`;
    modalMeta.textContent = `${movie.year} • ${movie.director} • ${movie.rating}/10`;
    modalAgeRating.textContent = `Age Rating: ${movie.ageRating}`;
    modalGenres.innerHTML = movie.genre.map(g => `<span class="tag">${g}</span>`).join('');
    modalDescription.textContent = movie.description;
    modalCast.textContent = movie.actors.join(', ');
    
    // Add producer information to modal
    let productionInfo = `Director: ${movie.director}`;
    if (movie.producers && movie.producers.length > 0) {
        productionInfo += `<br>Producers: ${movie.producers.join(', ')}`;
    }
    modalProduction.innerHTML = productionInfo;
    
    modal.style.display = 'block';
}

// Function to close movie modal
function closeMovieModal() {
    modal.style.display = 'none';
}

// Function to toggle filters visibility
function toggleFilters() {
    if (filtersSection.style.display === 'block') {
        filtersSection.style.display = 'none';
        filterArrow.classList.remove('rotate');
    } else {
        filtersSection.style.display = 'block';
        filterArrow.classList.add('rotate');
    }
}

// Function to reset all filters
function resetFilters() {
    mainSearch.value = '';
    document.getElementById('genre').value = '';
    document.getElementById('year').value = '';
    document.getElementById('rating').value = '';
    document.getElementById('age-rating').value = '';
    
    renderMovies(movies);
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initial render
    renderMovies(movies);
    
    // Toggle filters
    toggleFiltersButton.addEventListener('click', toggleFilters);
    
    // Search functionality
    searchButton.addEventListener('click', filterMovies);
    mainSearch.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            filterMovies();
        }
    });
    
    // Apply filters
    applyFiltersButton.addEventListener('click', filterMovies);
    
    // Reset filters
    resetFiltersButton.addEventListener('click', resetFilters);
    
    // Close modal when clicking the X
    closeModalButton.addEventListener('click', closeMovieModal);
    
    // Close modal when clicking outside the modal content
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            closeMovieModal();
        }
    });
});