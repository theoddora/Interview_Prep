import "./CharacterList.css";
import { useCharacters } from "../hooks/useCharactes";
import { Link } from "react-router";

export default function CharacterList() {
  const { error, data, loading } = useCharacters();
  console.log({ error, data, loading });

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Something went wrong.</div>;
  }

  return (
    <>
      <h1> Lenght is {data.characters.results.length}</h1>

      <div className="CharacterList">
        {data.characters.results.map((character: any) => {
          return (
            <Link key={character.id} to={`/${character.id}`}>
              <img src={character.image} alt={character.name} />
              <h2>{character.name}</h2>
            </Link>
          );
        })}
      </div>
    </>
  );
}
