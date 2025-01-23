import "./CharacterList.css";
import { useUser } from "../hooks/useUser";
import { Link } from "react-router";

export default function CharacterList() {
  const { error, data, loading } = useUser(1);
  console.log({ error, data, loading });

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Something went wrong.</div>;
  }

  return (
    <>
      {data && data.getUser && (
        <div className="CharacterList">
          <h1>
            User {data.getUser.username} with email {data.getUser.email}
          </h1>
          <ul>
            {data.getUser.posts.map((post: any) => (
              <li key={post.id}>
                <Link to={`/post/${post.id}`}>{post.title}</Link>
              </li>
            ))}
          </ul>
        </div>
      )}
    </>
  );
}
