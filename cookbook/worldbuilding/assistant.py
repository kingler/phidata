from typing import List, Optional

from phi.assistant import Assistant
from phi.llm.ollama import Ollama
from pydantic import BaseModel, Field


class World(BaseModel):
    planet: str = Field(
        ...,
        description="This is the planet our world is based on. Examples: Exa, Heras, Titan, Coruscant etc. Be as creative as possible. Do not use simple names like Futura, Earth, etc.",
    )
    population: int = Field(..., description="This is the population of the world.")
    characteristics: List[str] = Field(
        ...,
        description="These are the characteristics of the world. Examples: Magical, Advanced, Peaceful, Wartorn, Abundant, etc. Be as creative as possible.",
    )
    religions: List[str] = Field(
        ...,
        description="These are the religions followed by the people in the world. Examples: Sun Worship, Airbenders, etc.",
    )
    scandals: List[str] = Field(
        ...,
        description="These are the current scandals in the world. Think bollywood drama. Be as creative as possible.",
    )
    wars: List[str] = Field(
        ...,
        description="These are the old wars in the world. Think of how the world was shaped by these wars. Be as creative as possible.",
    )
    drugs: List[str] = Field(
        ..., description="These are the drugs the people in the world use. Be as creative as possible."
    )
    climate: str = Field(..., description="This is the climate of the world. Examples: Tropical, Desert, Arctic, etc.")
    cities: List[str] = Field(
        ..., description="These are the names of the cities in the world. Be as creative as possible."
    )
    languages: List[str] = Field(
        ..., description="These are the languages spoken in the world. Be as creative as possible."
    )
    history: str = Field(
        ...,
        description="This is the history of the world. Be as creative as possible. Use events, wars, etc. to make it interesting. Make it at least 100000 years old. Provide a detailed history.",
    )
    technology: str = Field(
        ..., description="This is the technology used in the world. Provide details. Be as creative as possible."
    )
    economy: str = Field(
        ..., description="This is the economy of the world. Provide details. Be as creative as possible."
    )
    timeline: str = Field(..., description="This is the timeline of the world.")
    power_structure: str = Field(..., description="This is the power structure of the world.")


def get_world_builder(
    model: str = "openhermes",
    temperature: float = 0.1,
    debug_mode: bool = False,
) -> Assistant:
    return Assistant(
        name="world_builder",
        llm=Ollama(model=model, options={"temperature": temperature}),
        description="You are an expert world builder designing an intricate and complex world.",
        instructions=[
            "You are tasked with creating a world with the following characteristics: "
            "planet, population, characteristics, religions, kingdoms, climate, cities, languages, history, technology, "
            "economy, timeline and power structure",
            "Your world should wow the reader and make them want to explore it.",
            "Be as creative as possible and think of unique and interesting characteristics for your world.",
        ],
        output_model=World,
        debug_mode=debug_mode,
    )


def get_world_explorer(
    world: World,
    model: str = "openhermes",
    temperature: float = 0.1,
    debug_mode: bool = False,
) -> Optional[Assistant]:
    if world is None:
        return None

    return Assistant(
        name="world_explorer",
        llm=Ollama(model=model, options={"temperature": temperature}),
        description="You are a world explorer that provides detailed information about a world.",
        instructions=[
            "You are tasked with answering questions about the world defined below in <world> tags",
            "Your job is to explore the intricacies of the world and provide detailed information about it.",
            "You an an explorer, a poet, a historian, a scientist, and a philosopher all rolled into one. You are the world's greatest expert on the world.",
            "Your answers should be creative, passionate, and detailed. You should make the reader want to explore the world.",
            "You should aim to wow the reader with the world's intricacies and make them want to explore it.",
            "Be as creative as possible and think of unique and interesting characteristics for the world.",
            "Always provide tidbits of information that make the world interesting and unique.",
            "Its ok to make up information about the world as long as it is consistent with the world's characteristics.",
            "Be as creative as possible and aim to wow the reader with the world's intricacies and make them want to explore it.",
        ],
        add_to_system_prompt=f"""
        <world>
        {world.model_dump_json(indent=4)}
        </world>
        """,
        debug_mode=debug_mode,
        add_chat_history_to_messages=True,
        num_history_messages=8,
    )
