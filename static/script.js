// selectors
let listItem = document.querySelectorAll('.list-item')
let pokeCry = document.querySelector('.poke-cry')
let pokeCryButton = document.querySelector('.poke-cry-button')
let selectSound = document.querySelector('.select-sound')
let pokeImage = document.querySelector('.poke-image')
let pokeId = document.querySelector('.poke-id')
let pokeName = document.querySelector('.poke-name')
let pokeHeight = document.querySelector('.poke-height')
let pokeWeight = document.querySelector('.poke-weight')
let pokeDescription = document.querySelector('.lower__content')
let pokeDescriptionP1 = document.querySelector('.poke-description-p1')
let pokeDescriptionP2 = document.querySelector('.poke-description-p2')
let pokeGenus = document.querySelector('.poke-genus')


// functions

const getPokemon = async (e) => {
	let entry = {
		data: e.innerHTML
	}

	await fetch(`/pokemon`, {
		method: "POST",
		credentials: "include",
		body: JSON.stringify(entry),
		cache: "no-cache",
		headers: new Headers({
			"content-type": "application/json"
		})
	})
	.then(function (response) {
		if (response.status !== 200) {
			console.log(`Looks like there was a problem. Status code: ${response.status}`);
			return;
		}
		response.json().then(function (data) {
			pokeCry.src = data['poke-cry'];
			pokeImage.src = data['image'];
			pokeId.innerHTML = data['poke-id'];
			pokeName.innerHTML = data['name'];
			pokeGenus.innerHTML = data['poke-genus'];
			pokeHeight.innerHTML = data['poke-height'];
			pokeWeight.innerHTML = data['poke-weight'];
			pokeDescriptionP1.innerHTML = data['poke-description-p1'];
			pokeDescriptionP2.innerHTML = data['poke-description-p2'];
		})
		.then(function () {
			pokeCry.load();
			pokeCry.play();
		})
	})
	.catch(function (error) {
		console.log("Fetch error: " + error);
	});
}

// event listeners

pokeCryButton.onclick = function() {
	pokeCry.load();
	pokeCry.play();
}

listItem.forEach(item => {
	item.addEventListener('click', e => {
		selectSound.play();
		pokeDescriptionP1.style.display = 'block';
		pokeDescriptionP2.style.display = 'none';
		clicked = false
		getPokemon(e.target)
	})
})

clicked = false
pokeDescription.onclick = function() {
	selectSound.play();
	if (clicked === false) {
		pokeDescriptionP1.style.display = 'none';
		pokeDescriptionP2.style.display = 'block';
		clicked = true
	} else {
		pokeDescriptionP1.style.display = 'block';
		pokeDescriptionP2.style.display = 'none';
		clicked = false
	}
}



