import React from 'react';
import PropTypes from 'prop-types';

class Likes extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    const { onLikeButtonClick } = this.props;
    onLikeButtonClick();
  }

  render() {
    const { likesCount, lognameLikesThis } = this.props;
    let icon;
    if (lognameLikesThis === 1) {
      icon = <i class="bi bi-heart-fill"></i>
    } else {
      icon = <i class="bi bi-heart"></i>
    }
    return (
      <div className="d-flex justify-content-between my-3 align-items-center">
        <a className="like-unlike-button icon-link link-danger" type="button" onClick={this.handleClick}>
          {icon}
        </a>
        <div>
          <strong>{likesCount + (likesCount === 1 ? ' like' : ' likes') }</strong>
        </div>
      </div>
    );
  }
}

Likes.propTypes = {
  onLikeButtonClick: PropTypes.func.isRequired,
  likesCount: PropTypes.number.isRequired,
  lognameLikesThis: PropTypes.number.isRequired,
};

export default Likes;
