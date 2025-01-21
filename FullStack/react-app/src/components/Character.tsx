import { useParams } from "react-router";
import { useCharacter } from "../hooks/useCharacter";
import "./Character.css";

function Character() {
  const { id } = useParams();
  if (!id) {
    return <div>No id provided</div>;
  }
  const { data, loading, error } = useCharacter(id);
  console.log({ data, loading, error });
  return (
    <div className="Character">
      {loading && <div>Loading...</div>}
      {error && <div>Something went wrong.</div>}
      {data && !data.character && <div>Character not found</div>}
      {data && data.character && (
        <>
          <h1>{data.character.name}</h1>
          <img src={data.character.image} alt={data.character.name} />
          <h2>Episodes</h2>
          <ul className="CharacterEpisodes">
            {data.character.episode.map((episode: any) => (
              <li key={episode.id}>
                {episode.name} - <b> {episode.episode}</b>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default Character;
