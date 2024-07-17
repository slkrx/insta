import React from 'react';
import PropTypes from 'prop-types';
import PostHeader from './header';
import Likes from './likes/likes';
import Comments from './comments/comments';

class Post extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      age: '',
      imgUrl: '',
      owner: '',
      ownerImgUrl: '',
      ownerShowUrl: '',
      postShowUrl: '',
      likesCount: 0,
      lognameLikesThis: 0,
    };
    this.onLikeButtonClick = this.onLikeButtonClick.bind(this);
  }

  componentDidMount() {
    const { url } = this.props;

    fetch(url, { credentials: 'include' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          age: data.age,
          imgUrl: data.img_url,
          owner: data.owner,
          ownerImgUrl: data.owner_img_url,
          ownerShowUrl: data.owner_show_url,
          postShowUrl: data.post_show_url,
        });
      })
      .catch((error) => console.log(error));

    fetch(`${url}likes/`, { credentials: 'include' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          likesCount: data.likes_count,
          lognameLikesThis: data.logname_likes_this,
        });
      })
      .catch((error) => console.log(error));
  }

  onLikeButtonClick() {
    const { lognameLikesThis } = this.state;
    const { url } = this.props;
    const likesUrl = `${url}likes/`;
    const headers = {
      method: lognameLikesThis === 1 ? 'DELETE' : 'POST',
      credentials: 'include',
    };
    const expectedStatus = lognameLikesThis === 1 ? 204 : 201;

    fetch(likesUrl, headers)
      .then((response) => {
        if (response.status !== expectedStatus) {
          throw Error(response.statusText);
        }
        this.setState((state) => ({
          lognameLikesThis: lognameLikesThis === 1 ? 0 : 1,
          likesCount: state.likesCount + (lognameLikesThis === 1 ? -1 : 1),
        }));
      });
  }

  render() {
    const {
      imgUrl, owner, age, ownerImgUrl, ownerShowUrl,
      postShowUrl, likesCount, lognameLikesThis,
    } = this.state;
    const { url } = this.props;

    let img;
    if (lognameLikesThis === 1) {
      img = <img src={imgUrl} alt="" class="rounded" width="100%"/>;
    } else {
      img = (
        <img
          src={imgUrl}
          alt=""
          onDoubleClick={this.onLikeButtonClick}
          class="rounded"
          width="100%"
        />
      );
    }

    return (
      <div className="post pb-4 border-bottom">
        <PostHeader
          owner={owner}
          age={age}
          ownerImgUrl={ownerImgUrl}
          ownerShowUrl={ownerShowUrl}
          postShowUrl={postShowUrl}
        />
        {img}
        <Likes
          likesCount={likesCount}
          lognameLikesThis={lognameLikesThis}
          onLikeButtonClick={this.onLikeButtonClick}
        />
        <Comments url={`${url}comments/`} />
      </div>
    );
  }
}

Post.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Post;
