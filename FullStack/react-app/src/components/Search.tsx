import { gql, useLazyQuery } from "@apollo/client";
import { useState } from "react";

const SEARCH_CHARACTER = gql`
  query SearchCharacter($name: String!) {
    characters(filter: { name: $name }) {
      results {
        location {
          name
        }
      }
    }
  }
`;

function Search() {
  const [name, setName] = useState("");

  const [getCharacterLocations, { error, data, loading, called }] =
    useLazyQuery(SEARCH_CHARACTER, {
      variables: {
        name,
      },
    });

  console.log({ error, data, loading, called });

  return (
    <div>
      <input value={name} onChange={(e) => setName(e.target.value)}></input>
      <button
        onClick={() => {
          console.log(name);
          getCharacterLocations();
        }}
      >
        Search
      </button>

      {loading && <div>Loading...</div>}
      {error && <div>Something went wrong.</div>}
      {data && !data.characters.results.length && <div>No results</div>}
      {data && data.characters.results.length && (
        <ul>
          {data.characters.results.map((character: any) => (
            <li key={character.location.name}>{character.location.name}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Search;
