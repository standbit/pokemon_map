import folium
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url),
            )

    pokemons_on_page = []

    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
            })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon_entities = PokemonEntity.objects.all()
    requested_pokemons = []
    for pokemon in pokemon_entities:
        if pokemon.pokemon.id == int(pokemon_id):
            requested_pokemons.append(pokemon)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemons:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    previous_evolution_img = ''
    if requested_pokemons[0].pokemon.previous_evolution:
        previous_evolution_img = request.build_absolute_uri(
            requested_pokemons[0].pokemon.previous_evolution.image.url)

    next_evolution_img = ''
    next_evolution_pokemon = None
    if requested_pokemons[0].pokemon.next_evolutions.all():
        next_evolution_pokemon = requested_pokemons[0].pokemon.next_evolutions.get()    # noqa E501
        next_evolution_img = request.build_absolute_uri(
            next_evolution_pokemon.image.url)

    pokemon = {
        "title_ru": requested_pokemons[0].pokemon.title,
        "img_url": request.build_absolute_uri(
            requested_pokemons[0].pokemon.image.url),
        "description": requested_pokemons[0].pokemon.description,
        "title_en": requested_pokemons[0].pokemon.title_en,
        "title_jp": requested_pokemons[0].pokemon.title_jp,
        "previous_evolution": requested_pokemons[0].pokemon.previous_evolution,
        "previous_evolution_img": previous_evolution_img,
        "next_evolution": next_evolution_pokemon,
        "next_evolution_img": next_evolution_img,
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
