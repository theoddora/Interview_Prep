import { useQuery, gql } from "@apollo/client";

const GET_USER = gql`
  query GetUser($id: Int!) {
    getUser(id: $id) {
      email
      id
      username
      posts {
        id
        title
        content
      }
    }
  }
`;

export const useUser = (id: number) => {
  const { error, data, loading } = useQuery(GET_USER, {
    variables: {
      id,
    },
  });
  return { error, data, loading };
};
