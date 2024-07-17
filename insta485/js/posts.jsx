import React from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import Post from './post/post';

class Posts extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      posts: [],
      next: '',
    };
    this.fetchPosts = this.fetchPosts.bind(this);
  }

  componentDidMount() {
    this.fetchPosts();
  }

  fetchPosts() {
    if (window.performance.getEntriesByType('navigation')[0].type === 'back_forward') {
      this.setState(window.history.state);
    } else {
      const { next } = this.state;
      const url = next || '/api/v1/p/';
      fetch(url, { credentials: 'include' })
        .then((response) => {
          if (!response.ok) {
            throw Error(response.statusText);
          }
          return response.json();
        })
        .then((data) => {
          this.setState((state) => ({
            posts: state.posts.concat(data.results),
            next: data.next,
          }));
          window.history.replaceState(this.state, 'saveState');
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }

  render() {
    const { posts, next } = this.state;
    return (
      <div>
        <InfiniteScroll
          dataLength={posts.length} // This is important field to render the next data
          next={this.fetchPosts}
          hasMore={next !== ''}
          loader={<h4>Loading...</h4>}
          endMessage={(
            <p style={{ textAlign: 'center' }}>
              <b>Yay! You have seen it all</b>
            </p>
          )}
        >
          {posts.map((post) => <Post url={post.url} key={post.postid} />)}
        </InfiniteScroll>
      </div>
    );
  }
}

export default Posts;
